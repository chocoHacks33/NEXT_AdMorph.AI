import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const apiKey = process.env.OPENAI_API_KEY;

  if (!apiKey) {
    return NextResponse.json(
      { error: 'OpenAI API key is not configured on the server.' },
      { status: 500 }
    );
  }

  try {
    const formData = await request.formData();
    const file = formData.get('file');

    if (!file) {
      return NextResponse.json({ error: 'No audio file provided.' }, { status: 400 });
    }

    // We need to reconstruct FormData to send to OpenAI
    const openAIFormData = new FormData();
    openAIFormData.append('file', file);
    openAIFormData.append('model', 'whisper-1');
    openAIFormData.append('language', 'en');
    openAIFormData.append('temperature', '0.0');
    openAIFormData.append('response_format', 'json');

    const openAIResponse = await fetch('https://api.openai.com/v1/audio/transcriptions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
      },
      body: openAIFormData,
    });

    if (!openAIResponse.ok) {
      const errorData = await openAIResponse.json().catch(() => ({}));
      console.error('OpenAI API Error:', errorData);
      return NextResponse.json(
        { 
          error: `Whisper API error: ${openAIResponse.status} ${openAIResponse.statusText}`,
          details: errorData
        },
        { status: openAIResponse.status }
      );
    }

    const data = await openAIResponse.json();
    return NextResponse.json({ transcript: data.text });

  } catch (error: unknown) {
    console.error('Error in /api/transcribe:', error);
    let errorMessage = 'An unknown error occurred during transcription.';
    if (error instanceof Error) {
      errorMessage = error.message;
    }
    return NextResponse.json({ error: errorMessage }, { status: 500 });
  }
}
