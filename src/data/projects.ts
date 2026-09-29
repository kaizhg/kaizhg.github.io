export type Discipline = 'ID' | 'CD' | 'IX';

export const disciplines: Record<Discipline, string> = {
	ID: 'Industrial',
	CD: 'Computational',
	IX: 'Interaction',
};

export interface Project {
	slug: string;
	title: string;
	year: number;
	discipline: Discipline;
	summary: string;
	context?: string;
	/** Case study on the old Adobe Portfolio site, until it is migrated. */
	legacyUrl: string;
}

export const projects: Project[] = [
	{
		slug: 'eyelash',
		title: '3D Printed Eyelash',
		year: 2024,
		discipline: 'ID',
		summary: '3D printed lash product',
		context: 'OPT Industries',
		legacyUrl: 'https://kaizhang.io/at-opt-industries',
	},
	{
		slug: 'os-11',
		title: 'Operating System 1.1',
		year: 2024,
		discipline: 'IX',
		summary: 'Interactive installation',
		legacyUrl: 'https://kaizhang.io/os-11',
	},
	{
		slug: 'large-language-objects',
		title: 'Large Language Objects',
		year: 2023,
		discipline: 'IX',
		summary: 'Physical interface design for LLMs',
		context: 'MIT HAN Lab',
		legacyUrl: 'https://kaizhang.io/large-language-objects',
	},
	{
		slug: 'inflatable-patterner',
		title: 'Inflatable Patterner',
		year: 2023,
		discipline: 'CD',
		summary: 'Grasshopper C# development',
		context: 'Pneuhaus',
		legacyUrl: 'https://kaizhang.io/inflatable-generator',
	},
	{
		slug: 'imago',
		title: 'Project Imago',
		year: 2023,
		discipline: 'CD',
		summary: 'Contemporary generative jewelry',
		legacyUrl: 'https://kaizhang.io/pupas',
	},
	{
		slug: 'hyperslice',
		title: 'HyperSlice',
		year: 2023,
		discipline: 'CD',
		summary: 'Image-interpolation-based 3D modeling workflow',
		legacyUrl: 'https://kaizhang.io/hyperslice',
	},
	{
		slug: 'seesaw',
		title: 'See/Saw',
		year: 2023,
		discipline: 'IX',
		summary: '1D balancing game and controller',
		legacyUrl: 'https://kaizhang.io/seesaw',
	},
	{
		slug: 'prismo',
		title: 'Prismo',
		year: 2022,
		discipline: 'ID',
		summary: 'Transformable lamp',
		legacyUrl: 'https://kaizhang.io/prismo',
	},
	{
		slug: 'yottabyte',
		title: 'Yottabyte',
		year: 2022,
		discipline: 'IX',
		summary: 'Interactive art on data consumption',
		legacyUrl: 'https://kaizhang.io/yotabyte',
	},
	{
		slug: 'mind-bridge',
		title: 'Mind Bridge',
		year: 2021,
		discipline: 'ID',
		summary: 'Wearable dataport',
		legacyUrl: 'https://kaizhang.io/mind-bridge',
	},
	{
		slug: 'telewind',
		title: 'TeleWind',
		year: 2021,
		discipline: 'IX',
		summary: 'Responsive telepresence furniture',
		legacyUrl: 'https://kaizhang.io/wind',
	},
	{
		slug: 'sound-x',
		title: 'Sound X 2021 Design R&D',
		year: 2020,
		discipline: 'ID',
		summary: 'Light effect design',
		context: 'Huawei CBG',
		legacyUrl: 'https://kaizhang.io/sound-x-2021-light-effect-design',
	},
	{
		slug: 'tables',
		title: 'Tables?',
		year: 2019,
		discipline: 'CD',
		summary: 'Generative furniture study',
		context: 'Zhang Zhoujie Digital Lab',
		legacyUrl: 'https://kaizhang.io/zhang-zhoujie-digital-lab-internship',
	},
];

/** Index code in the form DISCIPLINE.YEAR, e.g. IX.2023 */
export function projectCode(p: Project) {
	return `${p.discipline}.${p.year}`;
}
