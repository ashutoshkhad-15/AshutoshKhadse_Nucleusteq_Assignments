import { useRef } from 'react';

/**
 * Build a guarded submit handler for job create/edit forms.
 *
 * The returned handler mirrors the User module pattern: validate on submit,
 * surface field errors, and avoid duplicate in-flight submissions.
 *
 * @param {object} params - Submission dependencies.
 * @param {() => object} params.getValidationErrors - Callback returning the latest field errors.
 * @param {(errors: object) => void} params.setValidationErrors - Field error setter.
 * @param {(error: string | null) => void} params.setFormError - Form error setter.
 * @param {(payload: object) => Promise<void>} params.onSubmitValid - Async submit callback.
 * @returns {{ submittingRef: { current: boolean }, handleSubmit: (event: React.FormEvent<HTMLFormElement>) => Promise<void> }} Submission helpers.
 */
const useJobFormSubmission = ({ getValidationErrors, setValidationErrors, setFormError, onSubmitValid }) => {
    const submittingRef = useRef(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setFormError(null);

        if (submittingRef.current) {
            return;
        }

        const errors = getValidationErrors();
        if (Object.keys(errors).length > 0) {
            setValidationErrors(errors);
            return;
        }

        try {
            submittingRef.current = true;
            setValidationErrors({});
            await onSubmitValid();
        } finally {
            submittingRef.current = false;
        }
    };

    return { handleSubmit, submittingRef };
};

export default useJobFormSubmission;
