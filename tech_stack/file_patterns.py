FILE_PATTERNS = {
    # Configuration Files
    r"^package\.json$": ["npm", "nodejs"],
    r"^yarn\.lock$": ["yarn"],
    r"^pnpm-lock\.yaml$": ["pnpm"],
    r"^requirements\.txt$": ["pip", "python"],
    r"^Pipfile$": ["pipenv", "python"],
    r"^poetry\.lock$": ["poetry", "python"],
    r"^composer\.json$": ["composer", "php"],
    r"^Gemfile$": ["bundler", "ruby"],
    r"^go\.mod$": ["go_modules", "go"],
    r"^pom\.xml$": ["maven", "java"],
    r"^build\.gradle$": ["gradle", "java"],
    r"^Cargo\.toml$": ["cargo", "rust"],
    
    # Docker Files
    r"^Dockerfile$": ["docker"],
    r"^docker-compose\.ya?ml$": ["docker"],
    r"^\.dockerignore$": ["docker"],
    
    # CI/CD Files
    r"^\.github/workflows/.*\.ya?ml$": ["github_actions"],
    r"^\.gitlab-ci\.yml$": ["gitlab_ci"],
    r"^Jenkinsfile$": ["jenkins"],
    r"^\.travis\.yml$": ["travis"],
    r"^circle\.yml$": ["circleci"],
    r"^azure-pipelines\.yml$": ["azure_devops"],
    
    # Infrastructure as Code
    r".*\.tf$": ["terraform"],
    r"^terraform\.tfvars$": ["terraform"],
    r"^ansible\.cfg$": ["ansible"],
    r"^playbook\.ya?ml$": ["ansible"],
    
    # Kubernetes
    r".*k8s.*\.ya?ml$": ["kubernetes"],
    r".*kubernetes.*\.ya?ml$": ["kubernetes"],
    r"^deployment\.ya?ml$": ["kubernetes"],
    r"^service\.ya?ml$": ["kubernetes"],
    
    # Frontend Framework Files
    r"^next\.config\.js$": ["nextjs"],
    r"^nuxt\.config\.js$": ["nuxt"],
    r"^vue\.config\.js$": ["vue"],
    r"^angular\.json$": ["angular"],
    r"^svelte\.config\.js$": ["svelte"],
    r"^gatsby-config\.js$": ["gatsby"],
    r"^remix\.config\.js$": ["remix"],
    
    # Build Tool Configs
    r"^webpack\.config\.js$": ["webpack"],
    r"^vite\.config\.(js|ts)$": ["vite"],
    r"^rollup\.config\.js$": ["rollup"],
    r"^parcel\.config\.js$": ["parcel"],
    
    # Testing Configs
    r"^jest\.config\.(js|json)$": ["jest"],
    r"^cypress\.config\.(js|ts)$": ["cypress"],
    r"^playwright\.config\.(js|ts)$": ["playwright"],
    r"^vitest\.config\.(js|ts)$": ["vitest"],
    
    # Linting and Formatting
    r"^\.eslintrc.*$": ["eslint"],
    r"^\.prettierrc.*$": ["prettier"],
    r"^\.stylelintrc.*$": ["stylelint"],
    
    # Database
    r"^prisma/schema\.prisma$": ["prisma"],
    r"^migrations/.*\.sql$": ["database_migrations"],
    r"^seeds/.*\.(js|sql)$": ["database_migrations"],
    
    # Environment Files
    r"^\.env.*$": ["environment_config"],
    r"^\.env\.example$": ["environment_config"],
    
    # Documentation
    r"^swagger\.ya?ml$": ["swagger"],
    r"^openapi\.ya?ml$": ["openapi"],
    r"^README\.md$": ["documentation"],
    r"^docs/.*\.md$": ["documentation"],
    
    # Mobile Development
    r"^app\.json$": ["expo", "react_native"],
    r"^expo\.json$": ["expo"],
    r"^pubspec\.yaml$": ["flutter"],
    r"^ionic\.config\.json$": ["ionic"],
    
    # Cloud Platform Files
    r"^vercel\.json$": ["vercel"],
    r"^netlify\.toml$": ["netlify"],
    r"^railway\.json$": ["railway"],
    r"^render\.yaml$": ["render"],
    r"^heroku\.yml$": ["heroku"],
    
    # Serverless
    r"^serverless\.ya?ml$": ["serverless"],
    r"^sam\.ya?ml$": ["aws_sam"],
    r"^template\.ya?ml$": ["cloudformation"],
}

CONFIG_PATTERNS = {
    "tsconfig.json": ["typescript"],
    "babel.config.js": ["babel"],
    "tailwind.config.js": ["tailwindcss"],
    "postcss.config.js": ["postcss"],
    "nodemon.json": ["nodemon"],
    "pm2.config.js": ["pm2"],
    "nginx.conf": ["nginx"],
    "apache.conf": ["apache"],
    "redis.conf": ["redis"],
    "mongod.conf": ["mongodb"],
    "my.cnf": ["mysql"],
    "postgresql.conf": ["postgresql"],
}