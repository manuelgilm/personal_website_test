export interface Game {
  /** Stable identifier. */
  slug: string;
  /** Path (from site root) to the playable build, e.g. "play/snake/". */
  playPath: string;
  title: { en: string; es: string };
  description: { en: string; es: string };
  engine?: string;
  source?: string;
}

/**
 * Playable games shown on /games/.
 * Builds live in public/<playPath> (served at /play/<slug>/), excluded from indexing.
 * To add one: drop the export in public/play/<slug>/ and append an entry here.
 */
export const games: Game[] = [
  {
    slug: "snake",
    playPath: "play/snake/",
    title: { en: "Snake", es: "Snake" },
    description: {
      en: "A classic Snake remake built in Godot and exported for the web.",
      es: "Un remake del clásico Snake hecho en Godot y exportado para la web.",
    },
    engine: "Godot",
  },
];
