/**
 * It scrolls to the bottom of the page or a given element
 * @param {HTMLDivElement} [element] - The element to scroll to the bottom of. If not provided, the
 * window will be used.
 */
export const scrollToBottom = (element?: HTMLDivElement | Element) => {
  if (element)
    (element ?? window).scrollTo({
      top: element.scrollHeight,
      behavior: "smooth",
    });
};
