function getElementByIdOrThrow<T extends HTMLElement>(id: string): T {
  const el = document.getElementById(id);
  if (!el) throw new Error(`Element with id "${id}" not found`);
  return el as T;
}

export const selectedResourceLabel = getElementByIdOrThrow<HTMLSpanElement>("selectedResourceLabel");
export const pluginConfigurationDiv = getElementByIdOrThrow<HTMLDivElement>("configWarning");
export const existingIndexationsList = getElementByIdOrThrow<HTMLDivElement>("existingIndexationsList");
export const sidebar = getElementByIdOrThrow<HTMLDivElement>("sidebar");
export const openSidebarBtn = getElementByIdOrThrow<HTMLButtonElement>("openSidebarBtn");
export const selectOtherThesaurusBtn = getElementByIdOrThrow<HTMLButtonElement>("selectOtherThesaurusBtn");
export const thesaurusList = getElementByIdOrThrow<HTMLDivElement>("thesaurusList");
export const selectedThesaurusLabel = getElementByIdOrThrow<HTMLSpanElement>("selectedThesaurusLabel");
export const thesaurusLink = getElementByIdOrThrow<HTMLAnchorElement>("thesaurusLink");
export const searchInput = getElementByIdOrThrow<HTMLInputElement>("searchInput");
export const searchBtn = getElementByIdOrThrow<HTMLButtonElement>("searchBtn");
export const filterInput = getElementByIdOrThrow<HTMLInputElement>("filterInput");
export const searchResults = getElementByIdOrThrow<HTMLPreElement>("searchResults");