import { Eye, EyeOff } from 'lucide-react';

/**
 * Render a password input with a visibility toggle.
 *
 * @param {object} props - Component props.
 * @param {string} props.value - Current input value.
 * @param {(value: string) => void} props.onChange - Change handler for the field.
 * @param {string} props.placeholder - Placeholder text for the input.
 * @param {boolean} props.visible - Whether the password is shown in plain text.
 * @param {() => void} props.onToggleVisibility - Toggle callback for the icon button.
 * @param {boolean} props.disabled - Whether the input is disabled.
 * @param {string} props.toggleLabel - Accessible label for the toggle button.
 * @returns {JSX.Element} Password input control.
 */
const PasswordField = ({
    value,
    onChange,
    placeholder,
    visible,
    onToggleVisibility,
    disabled,
    toggleLabel,
}) => (
    <div className="password-field">
        <input
            type={visible ? 'text' : 'password'}
            className="input-field"
            placeholder={placeholder}
            value={value}
            onChange={(event) => onChange(event.target.value)}
            disabled={disabled}
        />
        <button
            type="button"
            className="input-toggle-btn"
            onClick={onToggleVisibility}
            aria-label={toggleLabel}
        >
            {visible ? <EyeOff size={16} /> : <Eye size={16} />}
        </button>
    </div>
);

export default PasswordField;
