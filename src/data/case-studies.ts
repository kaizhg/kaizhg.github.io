import type { ImageMetadata } from 'astro';

export interface ImageBlock {
	type: 'image';
	src: string; // path under src/assets/work/
	width: number;
	height: number;
	caption?: string;
}
export interface LoopBlock {
	type: 'loop';
	src: string; // public URL
	width: number;
	height: number;
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
	| { type: 'gallery'; items: MediaBlock[] }
	| { type: 'row'; columns: { flex: number; blocks: Block[] }[] };

export interface CaseStudy {
	slug: string;
	legacy: string;
	hero: MediaBlock | null;
	/** Gallery tile image and what it turns into on hover (from the old site's covers). */
	cover?: MediaBlock | null;
	hover?: MediaBlock | null;
	locked: boolean;
	blocks: Block[];
}

const studies = import.meta.glob<CaseStudy>('./case-studies/*.json', { eager: true, import: 'default' });
const images = import.meta.glob<ImageMetadata>('../assets/work/**/*.{jpg,png}', {
	eager: true,
	import: 'default',
});

export function getCaseStudy(slug: string): CaseStudy | undefined {
	return studies[`./case-studies/${slug}.json`];
}

export function workImage(src: string): ImageMetadata {
	const img = images[`../assets/work/${src}`];
	if (!img) throw new Error(`Missing work image: ${src}`);
	return img;
}
