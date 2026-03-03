"""
Markdown to Google Docs API batchUpdate request converter.

Converts markdown content (scripts, headings, bold, horizontal rules, etc.)
into Google Docs API requests for creating formatted documents.
"""

import re
from typing import List, Dict, Any, Tuple


def markdown_to_docs_requests(markdown: str) -> List[Dict[str, Any]]:
    """
    Convert markdown text into a list of Google Docs API batchUpdate requests.

    Returns a list of requests that should be applied via docs.documents.batchUpdate().
    Requests are built in reverse-insert order (bottom-up) so indices don't shift.
    """
    lines = markdown.split('\n')

    # First pass: build a list of segments with their formatting
    segments = _parse_markdown_lines(lines)

    # Second pass: convert segments into Docs API requests
    requests = _segments_to_requests(segments)

    return requests


def _parse_markdown_lines(lines: List[str]) -> List[Dict[str, Any]]:
    """Parse markdown lines into typed segments."""
    segments = []

    for line in lines:
        stripped = line.strip()

        # Horizontal rule
        if stripped in ('---', '***', '___') and len(stripped) >= 3:
            segments.append({'type': 'hr'})
            continue

        # Headings
        heading_match = re.match(r'^(#{1,3})\s+(.+)$', stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            segments.append({
                'type': 'heading',
                'level': level,
                'text': text,
            })
            continue

        # Checklist items
        checklist_match = re.match(r'^-\s*\[([ xX])\]\s*(.+)$', stripped)
        if checklist_match:
            checked = checklist_match.group(1).lower() == 'x'
            text = checklist_match.group(2)
            segments.append({
                'type': 'checklist',
                'checked': checked,
                'text': text,
            })
            continue

        # Regular text (including empty lines)
        segments.append({
            'type': 'text',
            'text': stripped,
        })

    return segments


def _segments_to_requests(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert parsed segments into Google Docs API requests.

    Strategy: Insert all text first, then apply formatting.
    We build the full document text and track where each segment lands,
    then generate formatting requests.
    """
    # Build the full text and track positions
    full_text = ''
    segment_positions = []  # (start_index, end_index, segment)

    for seg in segments:
        start = len(full_text) + 1  # +1 for 1-based Docs indexing

        if seg['type'] == 'hr':
            full_text += '\n'
            end = len(full_text) + 1
            segment_positions.append((start, end, seg))
        elif seg['type'] == 'heading':
            text = _strip_markdown_bold(seg['text'])
            full_text += text + '\n'
            end = len(full_text) + 1
            segment_positions.append((start, end, seg))
        elif seg['type'] == 'checklist':
            text = _strip_markdown_bold(seg['text'])
            full_text += text + '\n'
            end = len(full_text) + 1
            segment_positions.append((start, end, seg))
        elif seg['type'] == 'text':
            if seg['text'] == '':
                full_text += '\n'
                end = len(full_text) + 1
                segment_positions.append((start, end, seg))
            else:
                full_text += seg['text'] + '\n'
                end = len(full_text) + 1
                segment_positions.append((start, end, seg))

    # Now build the requests
    requests = []

    # 1. Insert all text at once
    if full_text:
        requests.append({
            'insertText': {
                'location': {'index': 1},
                'text': full_text,
            }
        })

    # 2. Apply formatting for each segment
    for start, end, seg in segment_positions:
        if seg['type'] == 'hr':
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'borderBottom': {
                            'color': {'color': {'rgbColor': {'red': 0.8, 'green': 0.8, 'blue': 0.8}}},
                            'width': {'magnitude': 1, 'unit': 'PT'},
                            'padding': {'magnitude': 6, 'unit': 'PT'},
                            'dashStyle': 'SOLID',
                        }
                    },
                    'fields': 'borderBottom',
                }
            })

        elif seg['type'] == 'heading':
            heading_map = {1: 'HEADING_1', 2: 'HEADING_2', 3: 'HEADING_3'}
            named_style = heading_map.get(seg['level'], 'HEADING_3')
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {'namedStyleType': named_style},
                    'fields': 'namedStyleType',
                }
            })
            # Apply bold formatting for any **bold** text within
            _add_inline_bold_requests(requests, seg['text'], start)

        elif seg['type'] == 'checklist':
            # Make it a checklist item
            requests.append({
                'createParagraphBullets': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'bulletPreset': 'BULLET_CHECKBOX',
                }
            })
            _add_inline_bold_requests(requests, seg['text'], start)

        elif seg['type'] == 'text' and seg['text']:
            text = seg['text']

            # Check for script section labels
            if _is_script_section_label(text):
                _add_section_label_formatting(requests, text, start)

            # Check for [TEXT OVERLAY: ...] patterns
            if '[TEXT OVERLAY:' in text.upper():
                _add_text_overlay_formatting(requests, text, start)

            # Apply inline bold formatting
            _add_inline_bold_requests(requests, text, start)

    return requests


def _strip_markdown_bold(text: str) -> str:
    """Remove ** markers from text, keeping the inner content."""
    return re.sub(r'\*\*(.+?)\*\*', r'\1', text)


def _add_inline_bold_requests(requests: List, text: str, line_start: int):
    """Find **bold** patterns in text and add bold formatting requests."""
    clean_text = _strip_markdown_bold(text)

    # Find bold segments in original text and map to clean text positions
    offset = 0
    for match in re.finditer(r'\*\*(.+?)\*\*', text):
        bold_text = match.group(1)
        # Find where this text appears in the clean version
        clean_pos = clean_text.find(bold_text, offset)
        if clean_pos >= 0:
            bold_start = line_start + clean_pos
            bold_end = bold_start + len(bold_text)
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': bold_start, 'endIndex': bold_end},
                    'textStyle': {'bold': True},
                    'fields': 'bold',
                }
            })
            offset = clean_pos + len(bold_text)


def _is_script_section_label(text: str) -> bool:
    """Check if a line starts with a script section label like HOOK, BODY, etc."""
    labels = ['HOOK A', 'HOOK B', 'HOOK C', 'BODY:', 'TEACH:', 'PUNCH:', 'CAPTION:']
    stripped = _strip_markdown_bold(text)
    return any(stripped.upper().startswith(label) for label in labels)


def _add_section_label_formatting(requests: List, text: str, line_start: int):
    """Add bold formatting to script section labels."""
    clean_text = _strip_markdown_bold(text)
    # Bold the label part (up to the first colon or parenthesis)
    label_match = re.match(r'^((?:HOOK [ABC]|BODY|TEACH|PUNCH|CAPTION)\s*(?:\([^)]*\))?:?)',
                           clean_text, re.IGNORECASE)
    if label_match:
        label_end = len(label_match.group(1))
        requests.append({
            'updateTextStyle': {
                'range': {'startIndex': line_start, 'endIndex': line_start + label_end},
                'textStyle': {'bold': True},
                'fields': 'bold',
            }
        })


def _add_text_overlay_formatting(requests: List, text: str, line_start: int):
    """Add bold + highlight formatting for [TEXT OVERLAY: ...] patterns."""
    clean_text = _strip_markdown_bold(text)
    for match in re.finditer(r'\[TEXT OVERLAY:\s*(.+?)\]', clean_text, re.IGNORECASE):
        overlay_start = line_start + match.start()
        overlay_end = line_start + match.end()
        requests.append({
            'updateTextStyle': {
                'range': {'startIndex': overlay_start, 'endIndex': overlay_end},
                'textStyle': {
                    'bold': True,
                    'backgroundColor': {
                        'color': {
                            'rgbColor': {'red': 1.0, 'green': 0.95, 'blue': 0.6}
                        }
                    },
                },
                'fields': 'bold,backgroundColor',
            }
        })
