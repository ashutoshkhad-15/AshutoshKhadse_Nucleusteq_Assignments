import { useEffect, useState } from 'react';

/**
 * Return a debounced version of a value that updates after the given delay.
 *
 * @param {*} value - The value to debounce.
 * @param {number} delay - Delay in milliseconds before the debounced value updates.
 * @returns {*} Debounced value.
 */
const useDebouncedValue = (value, delay = 800) => {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => {
            clearTimeout(timer);
        };
    }, [value, delay]);

    return debouncedValue;
};

export default useDebouncedValue;
