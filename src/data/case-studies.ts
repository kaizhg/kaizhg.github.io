import type { ImageMetadata } from 'astro';

export interface ImageBlock {
	type: 'image';
	src: string; // <slug>/<file> under content/
	width: number;
	height: number;
	caption?: string;
	/** The picture is a link */
	href?: string;
	/** Cap the rendered width (px) */
	maxWidth?: number;
	/** Cluster only: vertical offset in half-column units */
	y?: number;
	/** Tiny blurred stand-in (data URL) shown until the picture loads, and its edge colour */
	lqip?: string;
	tone?: string;
	/** Dark line art on a transparent ground: inverted on the dark theme */
	ink?: boolean;
	/** A second picture shown while the cursor is over this one (md: hover=file) */
	hover?: ImageBlock;
}
export interface LoopBlock {
	type: 'loop';
	src: string; // public URL
	width: number;
	height: number;
	poster?: string;
	lqip?: string;
	tone?: string;
}
export interface VideoBlock {
	type: 'video';
	src: string;
	poster: string;
	width: number;
	height: number;
	audio: boolean;
}
export type MediaBlock = ImageBlock | LoopBlock | VideoBlock;
export type Block =
	| MediaBlock
	| { type: 'text'; html: string }
	| { type: 'youtube'; id: string; start?: number }
	| { type: 'gallery'; items: MediaBlock[]; every?: number }
	| { type: 'cluster'; items: MediaBlock[] }
	| { type: 'row'; columns: { flex: number; blocks: Block[] }[] };

export interface CaseStudy {
	slug: string;
	legacy: string;
	hero: MediaBlock | null;
	/** Gallery tile image and what it turns into on hover (from the old site's covers). */
	cover?: MediaBlock | null;
	hover?: MediaBlock | null;
	/** The hero picture links here (front-matter `link`) */
	link?: string;
	/** 'wide' = two thirds of the page, 'half' = half, both left; default full */
	heroWidth?: 'full' | 'wide' | 'half';
	heroCaption?: string;
	locked: boolean;
	blocks: Block[];
}

const studies = import.meta.glob<CaseStudy>('./case-studies/*.json', { eager: true, import: 'default' });
const images = import.meta.glob<ImageMetadata>('../../content/**/*.{jpg,jpeg,png}', {
	eager: true,
	import: 'default',
});

export function getCaseStudy(slug: string): CaseStudy | undefined {
	return studies[`./case-studies/${slug}.json`];
}

export function workImage(src: string): ImageMetadata {
	const img = images[`../../content/${src}`];
	if (!img) throw new Error(`Missing work image: ${src}`);
	return img;
}
