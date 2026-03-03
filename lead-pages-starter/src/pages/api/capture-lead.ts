import type { APIRoute } from 'astro';
import { Client } from '@notionhq/client';

export const POST: APIRoute = async ({ request }) => {
  try {
    const { name, email, resource } = await request.json();

    // Validate inputs
    if (!name || !email || !resource) {
      return new Response(JSON.stringify({ error: 'Missing required fields' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    if (!email.includes('@') || !email.includes('.')) {
      return new Response(JSON.stringify({ error: 'Invalid email' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Access env vars dynamically
    const env = globalThis.process?.env ?? {};
    const apiKey = env['NOTION_API_KEY'] || import.meta.env.NOTION_API_KEY;
    const dbId = env['NOTION_LEADS_DB_ID'] || import.meta.env.NOTION_LEADS_DB_ID;

    if (!apiKey || !dbId || apiKey === 'your_notion_api_key_here') {
      // If Notion isn't configured, still return success (don't block the user)
      console.warn('Notion not configured — lead not saved');
      return new Response(JSON.stringify({ success: true, stored: false }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const notion = new Client({ auth: apiKey });

    await notion.pages.create({
      parent: { database_id: dbId },
      properties: {
        Name: { title: [{ text: { content: name } }] },
        Email: { email: email },
        Resource: { select: { name: resource } },
      },
    });

    return new Response(JSON.stringify({ success: true, stored: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    console.error('Lead capture error:', err);
    return new Response(JSON.stringify({ error: 'Server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
