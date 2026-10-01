export type Discipline = 'ID' | 'CD' | 'IX' | 'AR';

export const disciplines: Record<Discipline, string> = {
	ID: 'Industrial',
	CD: 'Computational',
	IX: 'Interaction',
	AR: 'Art',
};

export interface Project {
	slug: string;
	title: string;
	year: number;
	discipline: Discipline;
	summary: string;
	context?: string;
	/** Older and smaller work, shown after the selected projects. */
	archive?: boolean;
	/** Case study on the old Adobe Portfolio site, for reference. */
	legacyUrl: string;
}

// Generated from content/*/project.md by scripts/content.py — edit the markdown, not this list
import generated from './projects.json';

export const allProjects: Project[] = generated as Project[];
export const projects: Project[] = allProjects.filter((p) => !p.archive);
export const archive: Project[] = allProjects.filter((p) => p.archive);

export function projectCode(p: Project) {
	return String(p.year);
}
