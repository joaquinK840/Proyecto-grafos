import { useLayoutEffect, useState, type RefObject } from "react";

/** Width and height of an element in CSS pixels. */
export interface ElementSize {
  width: number;
  height: number;
}

/**
 * Track the size of an element.
 *
 * @param ref Ref attached to the element to measure.
 * @returns Its current size; `{0, 0}` until the element is mounted.
 *
 * How it works: the element is measured synchronously right after it is
 * mounted (layout effect), so the first paint already has a size and does
 * not depend on the first ResizeObserver notification, which some
 * environments deliver late. After that, a ResizeObserver keeps the size
 * updated when the layout changes.
 */
export function useElementSize(ref: RefObject<HTMLElement | null>): ElementSize {
  const [size, setSize] = useState<ElementSize>({ width: 0, height: 0 });

  useLayoutEffect(() => {
    const element = ref.current;
    if (!element) return;

    /**
     * Store a new size only when it changed, to avoid useless renders.
     *
     * @param width New width.
     * @param height New height.
     */
    const update = (width: number, height: number) =>
      setSize((previous) =>
        previous.width === width && previous.height === height ? previous : { width, height },
      );

    const bounds = element.getBoundingClientRect();
    update(bounds.width, bounds.height);

    const observer = new ResizeObserver(([entry]) => {
      update(entry.contentRect.width, entry.contentRect.height);
    });
    observer.observe(element);
    return () => observer.disconnect();
  }, [ref]);

  return size;
}
