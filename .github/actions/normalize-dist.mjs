/*
 * SPDX-License-Identifier: Apache-2.0
 */

import { readFile, writeFile } from "node:fs/promises";

const path = new URL("dist/index.js", `file://${process.cwd()}/`);
const source = await readFile(path, "utf8");
await writeFile(path, source.replace(/[\t ]+$/gm, ""));
