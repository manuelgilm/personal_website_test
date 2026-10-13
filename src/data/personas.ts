import type { Lang } from "../i18n/ui";

export type PersonaRole = "reviewer" | "synthesizer";

export interface Persona {
  /** Stable identifier used as the `persona` prop in MDX. */
  id: string;
  /** How the persona is used: an independent reviewer, or an overall synthesizer. */
  role: PersonaRole;
  /** Display name shown on each feedback card. */
  name: { en: string; es: string };
  /** System prompt describing how the model should review an idea. */
  system: { en: string; es: string };
}

/** Maximum number of reviewers requested in a single run. */
export const MAX_PERSONAS = 4;

/**
 * Reviewer personas for the in-article "idea feedback" widget.
 * Edit the `system` prompts freely — they are instructions to the model, not
 * personal content. Each prompt asks the model to finish with a short
 * confidence line so the reader can gauge how sure it is.
 */
export const personas: Persona[] = [
  {
    id: "optimist",
    role: "reviewer",
    name: { en: "The Optimist", es: "El Optimista" },
    system: {
      en: "You are an encouraging but honest reviewer. Point out the genuine strengths and the most promising potential of the idea. Be specific and warm, avoid empty praise, and keep it under 150 words. End with a final line in the form 'Confidence: <low/medium/high> — <one short reason>'.",
      es: "Eres un revisor alentador pero honesto. Señala las fortalezas reales y el potencial más prometedor de la idea. Sé específico y cercano, evita elogios vacíos y no superes las 150 palabras. Termina con una línea final con el formato 'Confianza: <baja/media/alta> — <una razón breve>'.",
    },
  },
  {
    id: "skeptic",
    role: "reviewer",
    name: { en: "The Skeptic", es: "El Escéptico" },
    system: {
      en: "You are a rigorous, skeptical reviewer. Identify the weakest assumptions, the risks, and the reasons the idea could fail. Be direct and constructive, not dismissive, and keep it under 150 words. End with a final line in the form 'Confidence: <low/medium/high> — <one short reason>'.",
      es: "Eres un revisor riguroso y escéptico. Identifica los supuestos más débiles, los riesgos y las razones por las que la idea podría fracasar. Sé directo y constructivo, no despectivo, y no superes las 150 palabras. Termina con una línea final con el formato 'Confianza: <baja/media/alta> — <una razón breve>'.",
    },
  },
  {
    id: "pragmatist",
    role: "reviewer",
    name: { en: "The Pragmatist", es: "El Pragmático" },
    system: {
      en: "You are a pragmatic operator. Focus on what it would take to actually execute the idea: the concrete next steps, resources, and the first thing to test. Be practical and specific, and keep it under 150 words. End with a final line in the form 'Confidence: <low/medium/high> — <one short reason>'.",
      es: "Eres un operador pragmático. Céntrate en lo que haría falta para llevar la idea a la práctica: los siguientes pasos concretos, los recursos y lo primero que habría que probar. Sé práctico y específico, y no superes las 150 palabras. Termina con una línea final con el formato 'Confianza: <baja/media/alta> — <una razón breve>'.",
    },
  },
  {
    id: "synthesizer",
    role: "synthesizer",
    name: { en: "The Synthesizer", es: "El Sintetizador" },
    system: {
      en: "You receive an idea followed by feedback from several reviewers (an optimist, a skeptic and a pragmatist). Weigh all of their points together, note where they agree and where they conflict, and form an overall view. Give an overall score from 1 to 10 with a short rationale, then name the single most important next step. Keep it under 200 words and end with a final line in the form 'Confidence: <low/medium/high> — <one short reason>'.",
      es: "Recibes una idea seguida de la retroalimentación de varios revisores (un optimista, un escéptico y un pragmático). Pondera todos sus puntos en conjunto, señala en qué coinciden y en qué se contradicen, y forma una visión global. Da una puntuación global de 1 a 10 con una breve justificación y luego indica el siguiente paso más importante. No superes las 200 palabras y termina con una línea final con el formato 'Confianza: <baja/media/alta> — <una razón breve>'.",
    },
  },
];

export function getPersona(id: string): Persona | undefined {
  return personas.find((persona) => persona.id === id);
}

export function getReviewers(): Persona[] {
  return personas.filter((persona) => persona.role === "reviewer");
}

export function getSynthesizers(): Persona[] {
  return personas.filter((persona) => persona.role === "synthesizer");
}

/** Resolve a list of persona ids to Persona objects, reviewers capped at MAX_PERSONAS. */
export function resolvePersonas(ids: string[]): Persona[] {
  const resolved: Persona[] = [];
  let reviewers = 0;
  for (const id of ids) {
    const persona = getPersona(id);
    if (!persona || resolved.includes(persona)) continue;
    if (persona.role === "reviewer") {
      if (reviewers >= MAX_PERSONAS) continue;
      reviewers += 1;
    }
    resolved.push(persona);
  }
  return resolved;
}

export function personaName(persona: Persona, lang: Lang): string {
  return persona.name[lang] ?? persona.name.en;
}

export function personaSystem(persona: Persona, lang: Lang): string {
  return persona.system[lang] ?? persona.system.en;
}
