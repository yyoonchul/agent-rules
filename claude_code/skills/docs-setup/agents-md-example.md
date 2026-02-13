# Example: Well-Written AGENTS.md

Below is an example of an `AGENTS.md` file.
It demonstrates how `AGENTS.md` acts as a "map".

---

# TaskFlow

> TaskFlow is a team project management SaaS. It consists of a Next.js web app and a PostgreSQL backend, supporting Stripe payments and real-time notifications.

## Tech Stack

- **Language**: TypeScript
- **Framework**: Next.js 15 (App Router), tRPC
- **Database**: PostgreSQL + Drizzle ORM
- **Infrastructure**: Vercel, Neon DB, Upstash Redis

## Directory Structure

```
src/
├── app/           # Next.js App Router pages
├── server/        # tRPC routers & business logic
├── db/            # Drizzle schema & migrations
├── lib/           # Shared utilities
└── components/    # UI components
```

## Documentation Navigation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture, domain boundaries, data flow |
| [docs/DESIGN.md](docs/DESIGN.md) | UI/UX design principles, component patterns |
| [docs/FRONTEND.md](docs/FRONTEND.md) | Frontend guidelines |
| [docs/design-docs/index.md](docs/design-docs/index.md) | List of design documents |
| [docs/product-specs/index.md](docs/product-specs/index.md) | List of product specs |
| [docs/PLANS.md](docs/PLANS.md) | Planning guidelines |

## Core Rules

1. All DB schema changes must have a design document written first.
2. All tRPC routers must include input validation (zod).
3. Components are separated into `components/ui/` (base) and `components/feature/` (domain).
4. Environment variables are managed type-safely in `env.ts`.
