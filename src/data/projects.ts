export interface Project {
  /** Stable identifier (used as a React-like key). */
  slug: string;
  /** Locale-less path to the project page. */
  href: string;
  title: { en: string; es: string };
  description: { en: string; es: string };
}

/**
 * Projects shown on /ai/projects/.
 * To add one: append an entry here and create the corresponding page
 * (e.g. src/pages/ai/projects/<slug>.astro + src/pages/es/ai/projects/<slug>.astro).
 */
export const projects: Project[] = [
  {
    slug: "mlflow",
    href: "ai/projects/mlflow",
    title: { en: "MLflow Server", es: "Servidor MLflow" },
    description: {
      en: "An open MLflow server for hands-on experiment tracking: register models, compare runs and explore the model registry.",
      es: "Un servidor de MLflow abierto para practicar el tracking de experimentos: registra modelos, compara ejecuciones y explora el registro de modelos.",
    },
  },
];
