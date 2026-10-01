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

const A = (p: Omit<Project, 'archive'>): Project => ({ ...p, archive: true });

/** Older and smaller work, in the order of the old site's Archive page. */
export const archive: Project[] = [
	A({ slug: 'transform', title: 'Transform', year: 2022, discipline: 'CD', summary: 'Grasshopper plugin for 1 DOF prismatic structures', legacyUrl: 'https://kaizhang.io/transform' }),
	A({ slug: 'vitalization', title: 'Vitalization', year: 2023, discipline: 'CD', summary: 'Generative study', legacyUrl: 'https://kaizhang.io/vitalization' }),
	A({ slug: 'ink-on-paper', title: 'Ink on Paper', year: 1999, discipline: 'AR', summary: 'Drawings and sketches', legacyUrl: 'https://kaizhang.io/drawing' }),
	A({ slug: 'marble-fall', title: 'Marble Fall', year: 2021, discipline: 'IX', summary: 'Multi-player AR game on wave function collapse', legacyUrl: 'https://kaizhang.io/marble-fall' }),
	A({ slug: 'made-in-gh', title: 'Made in GH', year: 2022, discipline: 'CD', summary: 'Explorations inside Grasshopper', legacyUrl: 'https://kaizhang.io/made-in-gh' }),
	A({ slug: 'briota-iospro', title: 'Briota IOSPro', year: 2023, discipline: 'ID', summary: 'Impulse oscillometry product design', legacyUrl: 'https://kaizhang.io/briota-iospro' }),
	A({ slug: 'hug', title: 'H U G', year: 2022, discipline: 'ID', summary: 'Pneumatic lamp and lightweight structure studies', legacyUrl: 'https://kaizhang.io/give-light-a-hug' }),
	A({ slug: 'invertebot', title: 'InverteBot', year: 2023, discipline: 'ID', summary: '"Informal" robot from a transformable prismatic structure', legacyUrl: 'https://kaizhang.io/invertebot' }),
	A({ slug: 'neurodynamic', title: 'Neurodynamic', year: 2019, discipline: 'ID', summary: 'Speculative wearable', legacyUrl: 'https://kaizhang.io/neurodynamic' }),
	A({ slug: 'dynamic-valley', title: 'Dynamic Valley', year: 2022, discipline: 'CD', summary: 'Mesh manipulation and motion visualization', legacyUrl: 'https://kaizhang.io/practice' }),
	A({ slug: 'homovirus', title: 'Homovirus', year: 2020, discipline: 'CD', summary: 'Digital sculpture and self-organizing behavior', legacyUrl: 'https://kaizhang.io/homovirus' }),
	A({ slug: 'providence-seat', title: 'Providence Station Seat', year: 2019, discipline: 'ID', summary: 'Public seating redesign', legacyUrl: 'https://kaizhang.io/providence-station-seat-redesign' }),
	A({ slug: 'mix-museum-guide', title: 'MIX Museum Guide', year: 2018, discipline: 'IX', summary: 'Mixed reality museum guide', legacyUrl: 'https://kaizhang.io/mix-musuem-guide' }),
	A({ slug: 'donut-in-half', title: 'Donut in Half', year: 2022, discipline: 'ID', summary: 'Object study', legacyUrl: 'https://kaizhang.io/donut' }),
	A({ slug: 'intersect', title: 'Intersect', year: 2022, discipline: 'ID', summary: 'Public restroom design', legacyUrl: 'https://kaizhang.io/intersect' }),
	A({ slug: 'barnacle-lamp', title: 'Barnacle Lamp', year: 2019, discipline: 'ID', summary: 'Lamp', legacyUrl: 'https://kaizhang.io/barnacle-lamp' }),
	A({ slug: 'rib-stool', title: 'Rib Stool', year: 2022, discipline: 'ID', summary: 'Lightweight stool', legacyUrl: 'https://kaizhang.io/rib-stool' }),
	A({ slug: 'folded-volume', title: 'Folded Volume', year: 2018, discipline: 'ID', summary: 'Sheet metal working', legacyUrl: 'https://kaizhang.io/metal' }),
	A({ slug: 'wood-ii', title: 'Wood II', year: 2019, discipline: 'ID', summary: 'Wood manipulation with machine tools', legacyUrl: 'https://kaizhang.io/wood-ii' }),
	A({ slug: 'wood-i', title: 'Wood I', year: 2018, discipline: 'ID', summary: 'Wood manipulation with hand tools', legacyUrl: 'https://kaizhang.io/wood' }),
	A({ slug: 'being-contained', title: 'Being Contained', year: 2018, discipline: 'AR', summary: 'Beginning hot glass', legacyUrl: 'https://kaizhang.io/being-contained' }),
	A({ slug: 'mix-headset', title: 'MIX Headset', year: 2018, discipline: 'ID', summary: 'SolidWorks practice', legacyUrl: 'https://kaizhang.io/mix-headset' }),
	A({ slug: 'mirrored-river', title: 'Mirrored River', year: 2019, discipline: 'AR', summary: 'Sculpture', legacyUrl: 'https://kaizhang.io/mirrored-river' }),
];

/** Every project, selected first. */
export const allProjects: Project[] = [...projects, ...archive];

/** Index code in the form DISCIPLINE.YEAR, e.g. IX.2023 */
export function projectCode(p: Project) {
	return String(p.year);
}
