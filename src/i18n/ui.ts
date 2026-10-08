export const languages = {
  en: "English",
  es: "Español",
} as const;

export const defaultLang = "en" as const;

export type Lang = keyof typeof languages;

export const locales = Object.keys(languages) as Lang[];

export const ui = {
  en: {
    "nav.home": "Home",
    "nav.ai": "AI & Engineering",
    "nav.ai.tutorials": "Tutorials",
    "nav.ai.articles": "Articles",
    "nav.ai.projects": "Projects",
    "nav.rides": "Road Trips",
    "nav.rides.routes": "Routes",
    "nav.rides.stories": "Stories",
    "nav.about": "About",
    "nav.contact": "Contact",
    "nav.cv": "CV",
    "nav.menu": "Menu",

    "lang.switch": "Select language",
    "theme.toggle": "Toggle theme",

    "home.title": "Manuel Gil | AI Platform Developer & MLOps Engineer",
    "home.description":
      "Personal site of Manuel Gil — AI Platform Developer and MLOps Engineer. Technical tutorials and articles, projects, and stories from the road.",
    "home.hero.kicker": "Hello, I'm",
    "home.hero.greeting": "I'm",
    "home.hero.roles":
      "Manuel Gil | An AI Platform Developer | An MLOps Engineer | A Software Builder | An Adventurer",
    "home.hero.title": "Manuel Gil",
    "home.hero.lead":
      "AI Platform Developer and MLOps Engineer",
    "home.hero.cta.ai": "AI & Engineering",
    "home.hero.cta.rides": "Road Trips",
    "home.latest": "Latest",

    "ai.title": "AI & Engineering | Manuel Gil",
    "ai.description":
      "Tutorials, articles and projects on data science, machine learning and AI engineering.",
    "ai.lead": "Tutorials, articles and projects on data science, machine learning and AI.",
    "ai.tutorials": "Tutorials",
    "ai.tutorials.description": "Structured, step-by-step tutorials and series.",
    "ai.articles": "Articles",
    "ai.articles.description":
      "Long-form articles, notes and experiments on data science, machine learning and AI engineering.",
    "ai.projects": "Projects",
    "ai.projects.description":
      "Tools and products I build and maintain, including the open MLflow experiment-tracking server.",
    "ai.watch": "Watch",
    "ai.watch.description": "Playlists and walkthroughs on my YouTube channel.",

    "rides.title": "Road Trips | Manuel Gil",
    "rides.description": "Motorcycle road trips: route guides and travel stories from the road.",
    "rides.lead": "Motorcycle road trips — routes, guides and stories from the road.",
    "rides.routes": "Routes",
    "rides.routes.description":
      "Route guides with maps, stops, timing and practical notes for motorcycle trips in Colombia.",
    "rides.stories": "Stories",
    "rides.stories.description":
      "Trip write-ups and photo journals from motorcycle journeys on the road.",

    "nav.games": "Games",
    "games.title": "Games | Manuel Gil",
    "games.description":
      "Game development by Manuel Gil: playable Godot games and devlogs on how they are built.",
    "games.lead": "Playable games, and devlogs on how I build them.",
    "games.overview": "Overview",
    "games.games": "Games",
    "games.play": "Play",
    "games.devlogs": "Devlogs",
    "games.devlogs.description":
      "Notes on building games — design, engines and lessons learned.",

    "about.title": "About | Manuel Gil",
    "about.description":
      "About Manuel Gil, an AI Platform Developer and MLOps Engineer based in Zipaquirá, Colombia.",
    "about.lead": "About",

    "contact.title": "Contact | Manuel Gil",
    "contact.description":
      "Get in touch with Manuel Gil for questions, collaborations or professional opportunities.",
    "contact.lead": "Get in touch",
    "contact.intro":
      "Have a question, an opportunity, or just want to say hi? Send me a message and I'll get back to you.",
    "contact.details.email": "Email",
    "contact.details.location": "Location",
    "contact.form.name": "Your name",
    "contact.form.email": "Your email",
    "contact.form.subject": "Subject",
    "contact.form.message": "Message",
    "contact.form.submit": "Send message",
    "contact.form.sending": "Sending…",
    "contact.form.success": "Your message has been sent. Thank you!",
    "contact.form.error.required": "Please fill in all fields.",
    "contact.form.error.email": "Please enter a valid email address.",
    "contact.form.error.generic": "Failed to send your message. Please try again.",
    "contact.form.error.network": "Failed to connect to the server. Please try again later.",
    "contact.thanks.title": "Message sent | Manuel Gil",
    "contact.thanks.lead": "Message sent",
    "contact.thanks.body": "Thanks for reaching out. I'll get back to you as soon as I can.",
    "contact.thanks.cta": "Back home",

    "cv.title": "CV | Manuel Gil",
    "cv.description":
      "CV of Manuel Gil — AI Platform Developer and MLOps Engineer: experience, skills, education and certifications.",
    "cv.download": "Download PDF",
    "cv.viewProjects": "View projects",
    "cv.summary": "Summary",
    "cv.experience": "Experience",
    "cv.skills": "Skills",
    "cv.education": "Education",
    "cv.certificates": "Certificates",

    "notfound.title": "Page not found | Manuel Gil",
    "notfound.description": "The page you are looking for does not exist.",
    "notfound.lead": "Page not found",
    "notfound.body": "The page you are looking for doesn't exist or has been moved.",
    "notfound.cta": "Back home",

    "footer.rights": "All rights reserved.",
    "footer.credits": "Built with Astro.",
    "common.soon": "Content coming soon.",
  },
  es: {
    "nav.home": "Inicio",
    "nav.ai": "IA e Ingeniería",
    "nav.ai.tutorials": "Tutoriales",
    "nav.ai.articles": "Artículos",
    "nav.ai.projects": "Proyectos",
    "nav.rides": "Viajes",
    "nav.rides.routes": "Rutas",
    "nav.rides.stories": "Historias",
    "nav.about": "Acerca de",
    "nav.contact": "Contacto",
    "nav.cv": "CV",
    "nav.menu": "Menú",

    "lang.switch": "Seleccionar idioma",
    "theme.toggle": "Cambiar tema",

    "home.title": "Manuel Gil | Desarrollador de Plataformas de IA e Ingeniero MLOps",
    "home.description":
      "Sitio personal de Manuel Gil — Desarrollador de Plataformas de IA e Ingeniero MLOps. Tutoriales y artículos técnicos, proyectos e historias de la carretera.",
    "home.hero.kicker": "Hola, soy",
    "home.hero.greeting": "Soy",
    "home.hero.roles":
      "Manuel Gil | Desarrollador de Plataformas de IA | Ingeniero MLOps | Creador de Software | Aventurero",
    "home.hero.title": "Manuel Gil",
    "home.hero.lead":
      "Desarrollador de Plataformas de IA e Ingeniero MLOps.",
    "home.hero.cta.ai": "IA e Ingeniería",
    "home.hero.cta.rides": "Viajes",
    "home.latest": "Recientes",

    "ai.title": "IA e Ingeniería | Manuel Gil",
    "ai.description":
      "Tutoriales, artículos y proyectos sobre ciencia de datos, machine learning e ingeniería de IA.",
    "ai.lead": "Tutoriales, artículos y proyectos sobre ciencia de datos, machine learning e IA.",
    "ai.tutorials": "Tutoriales",
    "ai.tutorials.description": "Tutoriales y series estructuradas, paso a paso.",
    "ai.articles": "Artículos",
    "ai.articles.description":
      "Artículos extensos, notas y experimentos sobre ciencia de datos, machine learning e ingeniería de IA.",
    "ai.projects": "Proyectos",
    "ai.projects.description":
      "Herramientas y productos que construyo y mantengo, incluido el servidor abierto de tracking de experimentos con MLflow.",
    "ai.watch": "Mira",
    "ai.watch.description": "Listas y recorridos en mi canal de YouTube.",

    "rides.title": "Viajes | Manuel Gil",
    "rides.description": "Viajes en moto: guías de ruta e historias desde la carretera.",
    "rides.lead": "Viajes en moto — rutas, guías e historias de la carretera.",
    "rides.routes": "Rutas",
    "rides.routes.description":
      "Guías de ruta con mapas, paradas, tiempos y notas prácticas para viajar en moto por Colombia.",
    "rides.stories": "Historias",
    "rides.stories.description":
      "Relatos de viaje y diarios fotográficos de recorridos en moto.",

    "nav.games": "Juegos",
    "games.title": "Juegos | Manuel Gil",
    "games.description":
      "Desarrollo de juegos de Manuel Gil: juegos jugables en Godot y devlogs sobre cómo se construyen.",
    "games.lead": "Juegos jugables y devlogs sobre cómo los construyo.",
    "games.overview": "Resumen",
    "games.games": "Juegos",
    "games.play": "Jugar",
    "games.devlogs": "Devlogs de juegos",
    "games.devlogs.description":
      "Notas sobre cómo construyo juegos: diseño, motores y lecciones aprendidas.",

    "about.title": "Acerca de | Manuel Gil",
    "about.description":
      "Acerca de Manuel Gil, Desarrollador de Plataformas de IA e Ingeniero MLOps en Zipaquirá, Colombia.",
    "about.lead": "Acerca de",

    "contact.title": "Contacto | Manuel Gil",
    "contact.description":
      "Ponte en contacto con Manuel Gil para preguntas, colaboraciones u oportunidades profesionales.",
    "contact.lead": "Ponte en contacto",
    "contact.intro":
      "¿Tienes una pregunta, una oportunidad o solo quieres saludar? Envíame un mensaje y te responderé.",
    "contact.details.email": "Correo",
    "contact.details.location": "Ubicación",
    "contact.form.name": "Tu nombre",
    "contact.form.email": "Tu correo",
    "contact.form.subject": "Asunto",
    "contact.form.message": "Mensaje",
    "contact.form.submit": "Enviar mensaje",
    "contact.form.sending": "Enviando…",
    "contact.form.success": "Tu mensaje ha sido enviado. ¡Gracias!",
    "contact.form.error.required": "Completa todos los campos.",
    "contact.form.error.email": "Ingresa un correo electrónico válido.",
    "contact.form.error.generic": "No se pudo enviar tu mensaje. Inténtalo de nuevo.",
    "contact.form.error.network": "No se pudo conectar con el servidor. Inténtalo más tarde.",
    "contact.thanks.title": "Mensaje enviado | Manuel Gil",
    "contact.thanks.lead": "Mensaje enviado",
    "contact.thanks.body": "Gracias por escribir. Te responderé lo antes posible.",
    "contact.thanks.cta": "Volver al inicio",

    "cv.title": "Currículum | Manuel Gil",
    "cv.description":
      "CV de Manuel Gil — Desarrollador de Plataformas de IA e Ingeniero MLOps: experiencia, habilidades, educación y certificaciones.",
    "cv.download": "Descargar PDF",
    "cv.viewProjects": "Ver proyectos",
    "cv.summary": "Resumen",
    "cv.experience": "Experiencia",
    "cv.skills": "Habilidades",
    "cv.education": "Educación",
    "cv.certificates": "Certificaciones",

    "notfound.title": "Página no encontrada | Manuel Gil",
    "notfound.description": "La página que buscas no existe.",
    "notfound.lead": "Página no encontrada",
    "notfound.body": "La página que buscas no existe o ha sido movida.",
    "notfound.cta": "Volver al inicio",

    "footer.rights": "Todos los derechos reservados.",
    "footer.credits": "Hecho con Astro.",
    "common.soon": "Contenido próximamente.",
  },
} as const;

export type UIKey = keyof (typeof ui)[typeof defaultLang];
