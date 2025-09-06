---
description: React project rules
globs: 
alwaysApply: false
---
## 🛠️ Frontend “Cursor Rules” — **React 19 + TypeScript + React Router DOM + Supabase**

> Use these guidelines when you create or review code for our web-novel platform. They replace the previous Next.js-focused rules.

---

### 📌 폴더 구조 핵심 원칙 (초기 단계)

1. **기능 중심**

   * 모든 새 코드는 `features/<feature-name>/` 아래에 모은다.

2. **필요할 때만 생성**

   * 폴더·파일은 “오늘 쓰는 것”만 만든다.

3. **단일 책임**

   * 컴포넌트·훅·API·서비스는 파일 1개당 역할 1개.

4. **내부 레이어**

   * 기능 폴더 안에서만 `ui/ hooks/ api/ services/ tests/` 분류한다.

5. **공통 코드 승격 규칙**

   * 동일 로직이 **3곳 이상** 재사용될 때만 `shared/`로 이동.

6. **상위 구조 고정**

   * 최상위는 딱 **`assets/ shared/ features/`** 세 폴더로 유지.

> 이 6가지만 지키면 MVP 속도와 향후 확장성을 동시에 확보할 수 있습니다.

# Project Frontend Rules

## UI 컴포넌트 사용 규칙

1. 공통 컴포넌트 우선 사용
   - src/shared/ui의 컴포넌트를 우선적으로 사용
   - Button, Card, Input, Badge 등 기본 컴포넌트 활용
   - 커스텀 스타일은 Tailwind 클래스로 적용

2. 문서 참조
   - docs/ui-guide.md 문서 먼저 확인
   - 컴포넌트 사용법 및 예시 코드 참고
   - 디자인 토큰 및 레이아웃 가이드라인 준수

3. 컴포넌트 Import 경로
   - 상대 경로 사용: "../../../shared/ui/[component]"
   - Path alias (@/) 사용 금지

4. 페이지 레이아웃
   - container + max-w-{size} 패턴 사용
   - 일관된 spacing system 적용
   - 반응형 디자인 고려

5. 상태 처리
   - 로딩/에러 상태 항상 구현
   - UI 가이드의 예시 활용

## 파일 구조

features/
  ├── [feature_1]]/
  │   ├── ui/          # 컴포넌트
  │   ├── hooks/       # 커스텀 훅
  │   ├── api/         # API 호출
  │   └── types/       # 타입 정의
  └── [feature_2]/
      ├── ui/
      ├── hooks/
      ├── api/
      └── types/

shared/
  ├── ui/             # 공통 컴포넌트
  ├── lib/            # 유틸리티
  ├── hooks/          # 공통 훅
  └── types/          # 공통 타입 
---

### 1. Code Style & Structure

| Theme                   | Guideline                                                                                                                                                     |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Language & Paradigm** | Write idiomatic **TypeScript** using *functional, declarative* React 19 patterns only—no class components.                                                    |
| **Type Safety**         | Provide full, explicit types; prefer **type aliases** & **interfaces** over `any`. Enable `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`. |
| **File/Folder Naming**  | `kebab-case` for folders, `PascalCase.tsx` for components, `camelCase.ts` for hooks & utils (`components/auth-wizard/AuthWizard.tsx`).                        |
| **Modularity**          | Break UI into small composable pieces. Put one React component or hook per file. Use barrel files (`index.ts`) only for public APIs.                          |
| **Utilities**           | Centralize helpers in `/lib` and shared hooks in `/hooks`. Keep each helper pure and side-effect-free.                                                        |

---

### 2. Routing & Navigation

* Use **React Router DOM v6** with data routers and `<Suspense>` for deferred/lazy data loading.
* colocate route components under `routes/` mirroring the URL structure.
* Favor **loader/actions** (v6.22+) to keep data fetching outside render paths and to enable optimistic UI.

---

### 3. State Management & Data Fetching

| Concern             | Guideline                                                                                                                                                    |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Global State**    | Use **Zustand** for non-server state (UI, feature flags). Keep each store flat & serializable.                                                               |
| **Server Data**     | Use **TanStack React Query** with Supabase RPC / SQL views. Define **query keys** in `/lib/queryKeys.ts`.                                                    |
| **Supabase Client** | Wrap `createClient()` in `/lib/supabaseBrowser.ts` and `/lib/supabaseServer.ts` (for Node scripts/tests) to avoid re-instantiation.                          |
| **Realtime**        | Use Supabase channel subscriptions inside custom hooks (`useChannel`) and expose snapshot state through TanStack Query’s `setQueryData` for cache coherence. |

---

### 4. Validation, Security & Error Handling

* **Zod** schemas for every external boundary (forms, route loaders, Supabase RPC payloads).
* Sanitize rich-text or user HTML with `sanitize-html`.
* Prevent XSS/CSRF:

  * Rely on Supabase’s **Row-Level Security (RLS)**—no direct `service_role` usage in the browser.
  * Use `SameSite=Lax` cookies for auth where needed.
* Apply **guard clauses** and throw custom `AppError` subclasses; catch with an `<ErrorBoundary>` per route.

---

### 5. Performance & Optimization

| Area                   | Practice                                                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Rendering**          | Leverage React 19 *compiler* (automatic memoization) where possible; avoid unnecessary `useEffect`.                       |
| **Code-Splitting**     | Use `React.lazy` + `Suspense` or `import()` inside route loaders; set webpack chunk names for clarity.                    |
| **Images**             | Import `.webp` or `.avif` only, specify `width`/`height`, enable `loading="lazy"` and decode using `fetchpriority="low"`. |
| **Caching**            | Configure React Query `staleTime` / `cacheTime` per use-case; prefer **server-side paging** in Supabase queries.          |
| **Accessibility & UX** | Default to **Radix Primitives** wrapped in **Shadcn UI** components; always set `aria-*` props.                           |

---

### 6. Styling System

* **Tailwind CSS** (JIT mode) — keep class lists short with `@apply` in component-scoped `*.module.css` when readability suffers.
* Use **CSS variables** for theme tokens; store them in `:root` and reference in Tailwind config.
* Follow a 4-point spacing scale (`1, 1.5, 2, 3, 4, 6, 8`).

---

### 7. Testing & Quality Gates

| Layer                  | Tools & Conventions                                                                                                               |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Unit / Integration** | **Jest** + **React Testing Library**; name files `*.test.tsx`. Mock Supabase with `@supabase/supabase-js` stubs.                  |
| **E2E**                | **Playwright**; tests run against local Supabase docker stack.                                                                    |
| **Coverage**           | Maintain ≥ 80 % statements; block PRs below threshold.                                                                            |
| **CI**                 | ESLint (`eslint-config-next` replaced with custom React 19 config), Prettier, TypeScript `--noEmit` type-check, Jest, Playwright. |

---

### 8. Documentation & Maintainability

* **JSDoc** on complex functions; keep them terse.
* Each folder has a `README.md` describing its public surface.
* Use **changesets** + **Conventional Commits** for versioning and automated changelog generation.
* Dependabot enabled; run `pnpm audit` in CI.

---

### 9. Output Expectations for New Code

1. **Type-safe, production-ready** React 19 functional components.
2. Supabase queries wrapped in React Query hooks with proper typing and optimistic updates.
3. Tailwind + Shadcn styled UI that is responsive and accessible.
4. Complete Zod validation and uniform error handling.
5. Corresponding Jest/RTL tests *and* Playwright E2E script skeletons.

> **Follow these rules rigorously** to ensure our codebase remains clean, secure, and scalable.
