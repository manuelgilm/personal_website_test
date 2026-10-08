export interface CvRole {
  title: string;
  company: string;
  period: string;
  bullets: string[];
}

export interface CvSkillGroup {
  group: string;
  items: string;
}

export interface CvEducation {
  degree: string;
  institution: string;
  period: string;
}

export interface CvCertificate {
  year: string;
  name: string;
}

export interface CvContent {
  summary: string;
  experience: CvRole[];
  skills: CvSkillGroup[];
  education: CvEducation[];
  certificates: CvCertificate[];
}

export const cv: Record<"en" | "es", CvContent> = {
  en: {
    summary:
      "MLOps and Machine Learning Engineer with strong experience designing, building, and supporting AI platforms that accelerate the development and productionization of machine learning solutions. Skilled in automation, orchestration, and scalable deployment of data and AI workflows. Proven track record in integrating machine learning platforms with governance and compliance frameworks, and in enabling cutting-edge AI capabilities such as large language model serving. Recognized for combining deep technical expertise with continuous learning, innovation, and a focus on building reliable, production-ready AI systems.",
    experience: [
      {
        title: "Machine Learning Engineer",
        company: "EPAM Systems",
        period: "Apr 2022 – Present",
        bullets: [
          "Developed a blueprint ML project using MLflow and Apache Spark, providing a reusable template to standardize future ML projects.",
          "Co-developed an AI platform (AAAI) enabling data scientists to develop and productionize ML projects across multiple environments (dev, QA, PROD) using Azure DevOps, Azure Databricks, and Azure Data Factory.",
          "Integrated New Relic monitoring into the AI platform to track and optimize job performance, improving reliability and visibility of workflows.",
          "Implemented Model Risk Governance (MRG) by integrating the platform with IBM OpenPages and AIFS, ensuring compliant model classification and risk-tiering.",
          "Automated creation of serving endpoints in Databricks via the Databricks AI Gateway, enabling AI Foundry LLMs to be exposed as production-ready services.",
          "Evaluating MLflow and Unity Catalog (UC) as the foundation for an enterprise-wide Agent Registry to standardize model and agent management.",
          "Provide ongoing support and continuous improvement for the AI platform and MRG integration, ensuring stability and adoption across teams.",
          "Designed and developed a modern ML platform implemented with DevOps Pipelines and Databricks Asset Bundles.",
        ],
      },
      {
        title: "Data Scientist",
        company: "DCKStudios",
        period: "May 2019 – Apr 2022",
        bullets: [
          "Applied data and process mining techniques to generate process flow models, providing actionable insights to guide future organizational decisions.",
          "Developed AI applications to enhance user experience, including speech-to-text, adult content detection, and brand/emotion recognition, leveraging Azure Custom Vision, OpenCV, image classification, object detection, and image processing.",
          "Built a machine learning solution for detecting water leaks in distribution networks using hydraulic simulations and reinforcement learning (Gym OpenAI).",
        ],
      },
    ],
    skills: [
      { group: "MLOps & ML Platforms", items: "MLflow, Databricks, Unity Catalog, Model Serving, Feature Engineering" },
      { group: "Cloud & DevOps", items: "Azure, CI/CD, DevOps Pipelines, Databricks Asset Bundles, Deployment Strategies" },
      { group: "Machine Learning", items: "Model Development, Machine Learning Engineering, Responsible AI" },
      { group: "Data & Analytics", items: "Data Understanding and Preparation, Data Mining" },
      { group: "APIs & Integration", items: "REST APIs, Platform Integration, Automation" },
    ],
    education: [
      {
        degree: "Bachelor of Electrical Engineering",
        institution: "Universidad de los Andes (VE)",
        period: "2011 – 2019",
      },
    ],
    certificates: [
      { year: "2023", name: "Databricks Certified Machine Learning Professional" },
      { year: "2023", name: "Databricks Academy Accreditation — Databricks Lakehouse Fundamentals" },
      { year: "2023", name: "Databricks Certified Machine Learning Associate" },
      { year: "2022", name: "Microsoft Certified: Azure Data Scientist Associate" },
    ],
  },
  es: {
    summary:
      "Ingeniero MLOps y de Machine Learning con amplia experiencia diseñando, construyendo y manteniendo plataformas de IA que aceleran el desarrollo y la puesta en producción de soluciones de machine learning. Hábil en automatización, orquestación y despliegue escalable de flujos de datos e IA. Trayectoria comprobada integrando plataformas de machine learning con marcos de gobernanza y cumplimiento, y habilitando capacidades de IA de vanguardia como el servicio de modelos de lenguaje (LLM). Reconocido por combinar experiencia técnica profunda con aprendizaje continuo, innovación y un enfoque en construir sistemas de IA confiables y listos para producción.",
    experience: [
      {
        title: "Ingeniero de Machine Learning",
        company: "EPAM Systems",
        period: "Abr 2022 – Presente",
        bullets: [
          "Desarrollé un proyecto de ML de referencia con MLflow y Apache Spark, aportando una plantilla reutilizable para estandarizar futuros proyectos de ML.",
          "Co-desarrollé una plataforma de IA (AAAI) que permite a los científicos de datos desarrollar y poner en producción proyectos de ML en múltiples entornos (dev, QA, PROD) usando Azure DevOps, Azure Databricks y Azure Data Factory.",
          "Integré el monitoreo de New Relic en la plataforma de IA para rastrear y optimizar el rendimiento de los jobs, mejorando la confiabilidad y visibilidad de los flujos.",
          "Implementé la Gobernanza de Riesgo de Modelos (MRG) integrando la plataforma con IBM OpenPages y AIFS, asegurando la clasificación de modelos y el tiering de riesgo conforme a la normativa.",
          "Automaticé la creación de endpoints de servicio en Databricks mediante el Databricks AI Gateway, permitiendo exponer los LLM de AI Foundry como servicios listos para producción.",
          "Evaluando MLflow y Unity Catalog (UC) como base para un Registro de Agentes empresarial que estandarice la gestión de modelos y agentes.",
          "Brindo soporte continuo y mejora sobre la plataforma de IA y la integración de MRG, asegurando estabilidad y adopción en los equipos.",
          "Diseñé y desarrollé una plataforma de ML moderna implementada con DevOps Pipelines y Databricks Asset Bundles.",
        ],
      },
      {
        title: "Científico de Datos",
        company: "DCKStudios",
        period: "May 2019 – Abr 2022",
        bullets: [
          "Apliqué técnicas de minería de datos y de procesos para generar modelos de flujo de procesos, aportando información accionable para guiar decisiones organizacionales.",
          "Desarrollé aplicaciones de IA para mejorar la experiencia de usuario, incluyendo speech-to-text, detección de contenido para adultos y reconocimiento de marca/emoción, usando Azure Custom Vision, OpenCV, clasificación de imágenes, detección de objetos y procesamiento de imágenes.",
          "Construí una solución de machine learning para detectar fugas de agua en redes de distribución usando simulaciones hidráulicas y aprendizaje por refuerzo (Gym OpenAI).",
        ],
      },
    ],
    skills: [
      { group: "MLOps y Plataformas de ML", items: "MLflow, Databricks, Unity Catalog, Model Serving, Feature Engineering" },
      { group: "Cloud y DevOps", items: "Azure, CI/CD, DevOps Pipelines, Databricks Asset Bundles, Estrategias de despliegue" },
      { group: "Machine Learning", items: "Desarrollo de modelos, Ingeniería de machine learning, IA responsable" },
      { group: "Datos y Analítica", items: "Entendimiento y preparación de datos, Minería de datos" },
      { group: "APIs e Integración", items: "REST APIs, Integración de plataformas, Automatización" },
    ],
    education: [
      {
        degree: "Ingeniero Eléctrico",
        institution: "Universidad de los Andes (VE)",
        period: "2011 – 2019",
      },
    ],
    certificates: [
      { year: "2023", name: "Databricks Certified Machine Learning Professional" },
      { year: "2023", name: "Databricks Academy Accreditation — Databricks Lakehouse Fundamentals" },
      { year: "2023", name: "Databricks Certified Machine Learning Associate" },
      { year: "2022", name: "Microsoft Certified: Azure Data Scientist Associate" },
    ],
  },
};
