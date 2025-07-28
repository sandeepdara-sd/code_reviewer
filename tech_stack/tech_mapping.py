ENHANCED_TECH_MAPPING = {
    # Frontend Frameworks
    "react": ("frontend", "frameworks", "React"),
    "next": ("frontend", "frameworks", "Next.js"),
    "nextjs": ("frontend", "frameworks", "Next.js"),
    "vue": ("frontend", "frameworks", "Vue.js"),
    "nuxt": ("frontend", "frameworks", "Nuxt.js"),
    "angular": ("frontend", "frameworks", "Angular"),
    "svelte": ("frontend", "frameworks", "Svelte"),
    "sveltekit": ("frontend", "frameworks", "SvelteKit"),
    "gatsby": ("frontend", "frameworks", "Gatsby"),
    "remix": ("frontend", "frameworks", "Remix"),
    
    # Frontend State Management
    "redux": ("frontend", "stateManagement", "Redux"),
    "zustand": ("frontend", "stateManagement", "Zustand"),
    "mobx": ("frontend", "stateManagement", "MobX"),
    "recoil": ("frontend", "stateManagement", "Recoil"),
    "jotai": ("frontend", "stateManagement", "Jotai"),
    "valtio": ("frontend", "stateManagement", "Valtio"),
    
    # Frontend Styling
    "tailwindcss": ("frontend", "styling", "Tailwind CSS"),
    "styled_components": ("frontend", "styling", "Styled Components"),
    "emotion": ("frontend", "styling", "Emotion"),
    "chakra_ui": ("frontend", "styling", "Chakra UI"),
    "material_ui": ("frontend", "styling", "Material-UI"),
    "mui": ("frontend", "styling", "MUI"),
    "antd": ("frontend", "styling", "Ant Design"),
    "bootstrap": ("frontend", "styling", "Bootstrap"),
    "bulma": ("frontend", "styling", "Bulma"),
    "semantic_ui": ("frontend", "styling", "Semantic UI"),
    
    # Frontend UI Libraries
    "mantine": ("frontend", "uiLibraries", "Mantine"),
    "react_bootstrap": ("frontend", "uiLibraries", "React Bootstrap"),
    "reactstrap": ("frontend", "uiLibraries", "Reactstrap"),
    "primereact": ("frontend", "uiLibraries", "PrimeReact"),
    "headlessui": ("frontend", "uiLibraries", "Headless UI"),
    "radix_ui": ("frontend", "uiLibraries", "Radix UI"),
    "arco_design": ("frontend", "uiLibraries", "Arco Design"),
    
    # Frontend Routing
    "react_router": ("frontend", "routing", "React Router"),
    "reach_router": ("frontend", "routing", "Reach Router"),
    "next_router": ("frontend", "routing", "Next.js Router"),
    "vue_router": ("frontend", "routing", "Vue Router"),
    
    # Frontend Build Tools
    "webpack": ("frontend", "buildTools", "Webpack"),
    "vite": ("frontend", "buildTools", "Vite"),
    "parcel": ("frontend", "buildTools", "Parcel"),
    "rollup": ("frontend", "buildTools", "Rollup"),
    "esbuild": ("frontend", "buildTools", "ESBuild"),
    "turbo": ("frontend", "buildTools", "Turbo"),
    
    # Frontend Form Handling
    "react_hook_form": ("frontend", "formHandling", "React Hook Form"),
    "formik": ("frontend", "formHandling", "Formik"),
    "final_form": ("frontend", "formHandling", "Final Form"),
    
    # Frontend Animation
    "framer_motion": ("frontend", "animation", "Framer Motion"),
    "react_spring": ("frontend", "animation", "React Spring"),
    "lottie_react": ("frontend", "animation", "Lottie React"),
    
    # Backend Frameworks
    "express": ("backend", "framework", "Express.js"),
    "fastapi": ("backend", "framework", "FastAPI"),
    "django": ("backend", "framework", "Django"),
    "flask": ("backend", "framework", "Flask"),
    "nestjs": ("backend", "framework", "NestJS"),
    "koa": ("backend", "framework", "Koa.js"),
    "hapi": ("backend", "framework", "Hapi.js"),
    "spring": ("backend", "framework", "Spring Boot"),
    "laravel": ("backend", "framework", "Laravel"),
    "symfony": ("backend", "framework", "Symfony"),
    "rails": ("backend", "framework", "Ruby on Rails"),
    "sinatra": ("backend", "framework", "Sinatra"),
    "gin": ("backend", "framework", "Gin"),
    "fiber": ("backend", "framework", "Fiber"),
    "echo": ("backend", "framework", "Echo"),
    
    # Backend Authentication
    "jsonwebtoken": ("backend", "authentication", "JWT"),
    "passport": ("backend", "authentication", "Passport.js"),
    "auth0": ("backend", "authentication", "Auth0"),
    "firebase_auth": ("backend", "authentication", "Firebase Auth"),
    "okta": ("backend", "authentication", "Okta"),
    "clerk": ("backend", "authentication", "Clerk"),
    "supabase": ("backend", "authentication", "Supabase Auth"),
    
    # Backend Validation
    "zod": ("backend", "validation", "Zod"),
    "joi": ("backend", "validation", "Joi"),
    "yup": ("backend", "validation", "Yup"),
    "ajv": ("backend", "validation", "AJV"),
    
    # Backend ORM
    "prisma": ("backend", "ORM", "Prisma"),
    "sequelize": ("backend", "ORM", "Sequelize"),
    "typeorm": ("backend", "ORM", "TypeORM"),
    "mongoose": ("backend", "ORM", "Mongoose"),
    "sqlalchemy": ("backend", "ORM", "SQLAlchemy"),
    "peewee": ("backend", "ORM", "Peewee"),
    "tortoise": ("backend", "ORM", "Tortoise ORM"),
    
    # Backend Job Scheduling
    "bullmq": ("backend", "jobScheduling", "BullMQ"),
    "node_cron": ("backend", "jobScheduling", "Node-cron"),
    "agenda": ("backend", "jobScheduling", "Agenda"),
    "celery": ("backend", "jobScheduling", "Celery"),
    
    # Database - Primary
    "pg": ("database", "primary", "PostgreSQL"),
    "postgresql": ("database", "primary", "PostgreSQL"),
    "mysql2": ("database", "primary", "MySQL"),
    "mysql": ("database", "primary", "MySQL"),
    "mongodb": ("database", "primary", "MongoDB"),
    "sqlite": ("database", "primary", "SQLite"),
    "sqlite3": ("database", "primary", "SQLite"),
    "mariadb": ("database", "primary", "MariaDB"),
    "oracle": ("database", "primary", "Oracle"),
    "mssql": ("database", "primary", "SQL Server"),
    
    # Database - Cache
    "redis": ("database", "cache", "Redis"),
    "memcached": ("database", "cache", "Memcached"),
    "elasticache": ("database", "cache", "ElastiCache"),
    
    # Database - Search
    "elasticsearch": ("database", "search", "Elasticsearch"),
    "opensearch": ("database", "search", "OpenSearch"),
    "solr": ("database", "search", "Apache Solr"),
    "algolia": ("database", "search", "Algolia"),
    
    # Database - Vector
    "pinecone": ("database", "vector", "Pinecone"),
    "weaviate": ("database", "vector", "Weaviate"),
    "chroma": ("database", "vector", "Chroma"),
    
    # DevOps - Containerization
    "docker": ("devops", "containerization", "Docker"),
    "podman": ("devops", "containerization", "Podman"),
    
    # DevOps - Orchestration
    "kubernetes": ("devops", "orchestration", "Kubernetes"),
    "docker_swarm": ("devops", "orchestration", "Docker Swarm"),
    "nomad": ("devops", "orchestration", "Nomad"),
    
    # DevOps - Infrastructure as Code
    "terraform": ("devops", "infrastructureAsCode", "Terraform"),
    "pulumi": ("devops", "infrastructureAsCode", "Pulumi"),
    "cloudformation": ("devops", "infrastructureAsCode", "CloudFormation"),
    "ansible": ("devops", "infrastructureAsCode", "Ansible"),
    
    # DevOps - CI/CD
    "github_actions": ("devops", "ciCd", "GitHub Actions"),
    "gitlab_ci": ("devops", "ciCd", "GitLab CI"),
    "jenkins": ("devops", "ciCd", "Jenkins"),
    "circleci": ("devops", "ciCd", "CircleCI"),
    "travis": ("devops", "ciCd", "Travis CI"),
    "azure_devops": ("devops", "ciCd", "Azure DevOps"),
    
    # DevOps - Monitoring
    "prometheus": ("devops", "monitoring", "Prometheus"),
    "grafana": ("devops", "monitoring", "Grafana"),
    "datadog": ("devops", "monitoring", "Datadog"),
    "newrelic": ("devops", "monitoring", "New Relic"),
    "sentry": ("devops", "monitoring", "Sentry"),
    "bugsnag": ("devops", "monitoring", "Bugsnag"),
    
    # DevOps - Logging
    "winston": ("devops", "logging", "Winston"),
    "pino": ("devops", "logging", "Pino"),
    "bunyan": ("devops", "logging", "Bunyan"),
    "loguru": ("devops", "logging", "Loguru"),
    "elk": ("devops", "logging", "ELK Stack"),
    
    # DevOps - Web Servers
    "nginx": ("devops", "webServer", "Nginx"),
    "apache": ("devops", "webServer", "Apache"),
    "caddy": ("devops", "webServer", "Caddy"),
    
    # Cloud Providers
    "aws_sdk": ("cloud", "provider", "AWS"),
    "boto3": ("cloud", "provider", "AWS"),
    "google_cloud": ("cloud", "provider", "Google Cloud Platform"),
    "azure": ("cloud", "provider", "Microsoft Azure"),
    "digitalocean": ("cloud", "provider", "DigitalOcean"),
    "linode": ("cloud", "provider", "Linode"),
    "vultr": ("cloud", "provider", "Vultr"),
    
    # Cloud Services
    "aws_lambda": ("cloud", "serverless", "AWS Lambda"),
    "vercel": ("cloud", "hosting", "Vercel"),
    "netlify": ("cloud", "hosting", "Netlify"),
    "heroku": ("cloud", "hosting", "Heroku"),
    "railway": ("cloud", "hosting", "Railway"),
    "render": ("cloud", "hosting", "Render"),
    
    # AI/ML Libraries
    "tensorflow": ("ai_ml", "libraries", "TensorFlow"),
    "pytorch": ("ai_ml", "libraries", "PyTorch"),
    "scikit_learn": ("ai_ml", "libraries", "Scikit-learn"),
    "pandas": ("ai_ml", "libraries", "Pandas"),
    "numpy": ("ai_ml", "libraries", "NumPy"),
    "opencv": ("ai_ml", "libraries", "OpenCV"),
    "huggingface": ("ai_ml", "libraries", "Hugging Face"),
    "langchain": ("ai_ml", "libraries", "LangChain"),
    "openai": ("ai_ml", "apis", "OpenAI API"),
    "anthropic": ("ai_ml", "apis", "Anthropic API"),
    "cohere": ("ai_ml", "apis", "Cohere API"),
    
    # Mobile Development
    "react_native": ("mobile", "framework", "React Native"),
    "expo": ("mobile", "framework", "Expo"),
    "flutter": ("mobile", "framework", "Flutter"),
    "ionic": ("mobile", "framework", "Ionic"),
    "xamarin": ("mobile", "framework", "Xamarin"),
    "cordova": ("mobile", "framework", "Apache Cordova"),
    
    # Testing - Unit
    "jest": ("testing", "unit", "Jest"),
    "mocha": ("testing", "unit", "Mocha"),
    "jasmine": ("testing", "unit", "Jasmine"),
    "vitest": ("testing", "unit", "Vitest"),
    "pytest": ("testing", "unit", "PyTest"),
    "unittest": ("testing", "unit", "unittest"),
    "phpunit": ("testing", "unit", "PHPUnit"),
    "rspec": ("testing", "unit", "RSpec"),
    
    # Testing - Integration
    "supertest": ("testing", "integration", "SuperTest"),
    "chai": ("testing", "integration", "Chai"),
    
    # Testing - E2E
    "cypress": ("testing", "e2e", "Cypress"),
    "playwright": ("testing", "e2e", "Playwright"),
    "puppeteer": ("testing", "e2e", "Puppeteer"),
    "selenium": ("testing", "e2e", "Selenium"),
    "webdriver": ("testing", "e2e", "WebDriver"),
    
    # Testing - Mocking
    "sinon": ("testing", "mocking", "Sinon.js"),
    "nock": ("testing", "mocking", "Nock"),
    "msw": ("testing", "mocking", "Mock Service Worker"),
    
    # Testing - Coverage
    "istanbul": ("testing", "coverage", "Istanbul"),
    "nyc": ("testing", "coverage", "NYC"),
    "codecov": ("testing", "coverage", "Codecov"),
    
    # Security
    "helmet": ("security", "headers", "Helmet.js"),
    "bcrypt": ("security", "encryption", "bcrypt"),
    "crypto": ("security", "encryption", "Crypto"),
    "cors": ("security", "cors", "CORS"),
    "express_rate_limit": ("security", "rateLimiting", "Express Rate Limit"),
    
    # Real-time Communication
    "socket.io": ("realtime", "websockets", "Socket.io"),
    "ws": ("realtime", "websockets", "WebSocket"),
    "pusher": ("realtime", "service", "Pusher"),
    "ably": ("realtime", "service", "Ably"),
    
    # External Integrations - Payments
    "stripe": ("externalIntegrations", "payments", "Stripe"),
    "paypal": ("externalIntegrations", "payments", "PayPal"),
    "square": ("externalIntegrations", "payments", "Square"),
    "razorpay": ("externalIntegrations", "payments", "Razorpay"),
    
    # External Integrations - Email
    "sendgrid": ("externalIntegrations", "email", "SendGrid"),
    "mailgun": ("externalIntegrations", "email", "Mailgun"),
    "postmark": ("externalIntegrations", "email", "Postmark"),
    "nodemailer": ("externalIntegrations", "email", "Nodemailer"),
    
    # External Integrations - SMS
    "twilio": ("externalIntegrations", "sms", "Twilio"),
    "vonage": ("externalIntegrations", "sms", "Vonage"),
    
    # External Integrations - File Storage
    "aws_s3": ("externalIntegrations", "fileStorage", "AWS S3"),
    "cloudinary": ("externalIntegrations", "fileStorage", "Cloudinary"),
    "uploadcare": ("externalIntegrations", "fileStorage", "Uploadcare"),
    
    # External Integrations - Analytics
    "google_analytics": ("externalIntegrations", "analytics", "Google Analytics"),
    "mixpanel": ("externalIntegrations", "analytics", "Mixpanel"),
    "amplitude": ("externalIntegrations", "analytics", "Amplitude"),
    "segment": ("externalIntegrations", "analytics", "Segment"),
    
    # Documentation
    "swagger": ("documentation", "apiDocs", "Swagger"),
    "openapi": ("documentation", "apiDocs", "OpenAPI"),
    "postman": ("documentation", "apiDocs", "Postman"),
    "insomnia": ("documentation", "apiDocs", "Insomnia"),
    "docusaurus": ("documentation", "projectDocs", "Docusaurus"),
    "gitbook": ("documentation", "projectDocs", "GitBook"),
    "notion": ("documentation", "projectDocs", "Notion"),
    
    # API Technologies
    "graphql": ("api", "queryLanguage", "GraphQL"),
    "apollo": ("api", "graphql", "Apollo"),
    "relay": ("api", "graphql", "Relay"),
    "rest": ("api", "architecture", "REST"),
    "grpc": ("api", "protocol", "gRPC"),
    "trpc": ("api", "framework", "tRPC"),
    
    # Message Queues
    "rabbitmq": ("messaging", "queue", "RabbitMQ"),
    "apache_kafka": ("messaging", "streaming", "Apache Kafka"),
    "aws_sqs": ("messaging", "queue", "AWS SQS"),
    "azure_service_bus": ("messaging", "queue", "Azure Service Bus"),
    
    # Package Managers
    "npm": ("projectMeta", "packageManagers", "NPM"),
    "yarn": ("projectMeta", "packageManagers", "Yarn"),
    "pnpm": ("projectMeta", "packageManagers", "PNPM"),
    "pip": ("projectMeta", "packageManagers", "Pip"),
    "pipenv": ("projectMeta", "packageManagers", "Pipenv"),
    "poetry": ("projectMeta", "packageManagers", "Poetry"),
    "conda": ("projectMeta", "packageManagers", "Conda"),
    "composer": ("projectMeta", "packageManagers", "Composer"),
    "bundler": ("projectMeta", "packageManagers", "Bundler"),
    "maven": ("projectMeta", "packageManagers", "Maven"),
    "gradle": ("projectMeta", "packageManagers", "Gradle"),
    "go_modules": ("projectMeta", "packageManagers", "Go Modules"),
    
    # Languages
    "typescript": ("projectMeta", "languagesUsed", "TypeScript"),
    "javascript": ("projectMeta", "languagesUsed", "JavaScript"),
    "python": ("projectMeta", "languagesUsed", "Python"),
    "java": ("projectMeta", "languagesUsed", "Java"),
    "go": ("projectMeta", "languagesUsed", "Go"),
    "rust": ("projectMeta", "languagesUsed", "Rust"),
    "ruby": ("projectMeta", "languagesUsed", "Ruby"),
    "php": ("projectMeta", "languagesUsed", "PHP"),
    "csharp": ("projectMeta", "languagesUsed", "C#"),
    "swift": ("projectMeta", "languagesUsed", "Swift"),
    "kotlin": ("projectMeta", "languagesUsed", "Kotlin"),
    
    # Structure indicators
    "react_structure": ("frontend", "frameworks", "React"),
    "nextjs_structure": ("frontend", "frameworks", "Next.js"),
    "component_architecture": ("frontend", "architecture", "Component-based"),
    "database_migrations": ("backend", "database", "Database Migrations"),
    "react_hooks": ("frontend", "patterns", "React Hooks"),
    "database_implied": ("database", "usage", "Database Usage Detected"),
}
