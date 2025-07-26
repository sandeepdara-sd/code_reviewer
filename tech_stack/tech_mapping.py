# This dictionary maps keywords/library names to their category in the tech stack.
# Format: "keyword": ("Category", "SubCategory", "TechnologyName")
TECH_MAPPING = {
    # Frontend
    "react": ("frontend", "frameworks", "React"),
    "next": ("frontend", "frameworks", "Next.js"),
    "vue": ("frontend", "frameworks", "Vue.js"),
    "angular": ("frontend", "frameworks", "Angular"),
    "redux": ("frontend", "stateManagement", "Redux"),
    "zustand": ("frontend", "stateManagement", "Zustand"),
    "tailwindcss": ("frontend", "styling", "Tailwind CSS"),
    "react-router": ("frontend", "routing", "React Router"),
    "next-router": ("frontend", "routing", "Next.js Routing"),
    "react-hook-form": ("frontend", "formHandling", "React Hook Form"),
    "i18next": ("frontend", "i18n", "i18next"),
    "webpack": ("frontend", "buildTools", "Webpack"),
    "vite": ("frontend", "buildTools", "Vite"),

    # Backend
    "express": ("backend", "framework", "Express.js"),
    "fastapi": ("backend", "framework", "FastAPI"),
    "django": ("backend", "framework", "Django"),
    "flask": ("backend", "framework", "Flask"),
    "jsonwebtoken": ("backend", "authentication", "JWT"),
    "firebase-admin": ("backend", "authentication", "Firebase Auth"),
    "zod": ("backend", "validation", "Zod"),
    "joi": ("backend", "validation", "Joi"),
    "prisma": ("backend", "ORM", "Prisma"),
    "bullmq": ("backend", "jobScheduling", "BullMQ"),
    "node-cron": ("backend", "jobScheduling", "Node-cron"),

    # Database
    "pg": ("database", "primary", "PostgreSQL"),
    "mysql2": ("database", "primary", "MySQL"),
    "mongodb": ("database", "primary", "MongoDB"),
    "redis": ("database", "cache", "Redis"),
    "elasticsearch": ("database", "search", "Elasticsearch"),

    # DevOps
    "docker": ("devops", "containerization", "Docker"),
    "kubernetes": ("devops", "orchestration", "Kubernetes"),
    "terraform": ("devops", "infrastructureAsCode", "Terraform"),
    "winston": ("devops", "logging", "Winston"),
    "prometheus": ("devops", "monitoring", "Prometheus"),
    "grafana": ("devops", "monitoring", "Grafana"),

    # Cloud (Identified by SDKs)
    "aws-sdk": ("cloud", "provider", "AWS"),
    "@google-cloud/storage": ("cloud", "provider", "GCP"),
    "@azure/storage-blob": ("cloud", "provider", "Azure"),

    # AI/ML
    "tensorflow": ("ai_ml", "libraries", "TensorFlow"),
    "scikit-learn": ("ai_ml", "libraries", "Scikit-learn"),
    "openai": ("ai_ml", "libraries", "OpenAI API"),

    # Mobile
    "react-native": ("mobile", "framework", "React Native"),

    # Testing
    "jest": ("testing", "unit", "Jest"),
    "mocha": ("testing", "unit", "Mocha"),
    "cypress": ("testing", "e2e", "Cypress"),
    "sinon": ("testing", "mocking", "Sinon.js"),
    "istanbul": ("testing", "coverage", "Istanbul"),

    # Security
    "helmet": ("security", "headers", "Helmet.js"),
    "bcrypt": ("security", "encryption", "bcrypt"),

    # Realtime
    "socket.io": ("realtime", "tech", "Socket.io"),

    # External Integrations
    "stripe": ("externalIntegrations", "payments", "Stripe"),
    "sendgrid": ("externalIntegrations", "email", "SendGrid"),
    "aws-s3": ("externalIntegrations", "fileStorage", "AWS S3"),

    # Documentation
    "swagger-ui-express": ("documentation", "apiDocs", "Swagger"),
    "docusaurus": ("documentation", "projectDocs", "Docusaurus"),

    # Project Meta
    "npm": ("projectMeta", "packageManagers", "NPM"),
    "yarn": ("projectMeta", "packageManagers", "Yarn"),
    "pip": ("projectMeta", "packageManagers", "Pip"),
    "typescript": ("projectMeta", "languagesUsed", "TypeScript"),
}