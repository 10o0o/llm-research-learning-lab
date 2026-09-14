export interface MockEntry {
  id: string;
  body?: string;
  data: {
    title: string;
    updated: string | Date;
    tags: string[];
  };
}

export type CollectionEntry<_CollectionName extends string = string> = MockEntry;

let entries: MockEntry[] = [];

export function setMockCollectionEntries(nextEntries: MockEntry[]): void {
  entries = nextEntries;
}

export async function getCollection(
  _collectionName?: string,
): Promise<CollectionEntry[]> {
  return entries;
}
