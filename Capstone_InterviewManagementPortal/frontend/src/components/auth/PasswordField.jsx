import { Eye, EyeOff } from 'lucide-react';

/**
 * Render a password input with a visibility toggle.
 */
const PasswordField = ({
    id,
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
            id={id}
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
