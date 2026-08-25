/**
 * FACILITATOR ONLY.
 *
 * Runs bugcheck/seeded-bugs.spec.ts — tests that assert the CORRECT behaviour and
 * therefore FAIL against the seeded app. Nine failures is the expected result and is
 * your proof that the planted defects listed in facilitator/SEEDED-BUGS.md are still
 * live.
 *
 *   npx playwright test -c pw-bugcheck.config.ts
 *
 * Not part of `npm test`.
 */
import { defineConfig } from '@playwright/test';
import base from './playwright.config';

export default defineConfig({
  ...base,
  testDir: './bugcheck',
  reporter: 'line',
  retries: 0,
});
