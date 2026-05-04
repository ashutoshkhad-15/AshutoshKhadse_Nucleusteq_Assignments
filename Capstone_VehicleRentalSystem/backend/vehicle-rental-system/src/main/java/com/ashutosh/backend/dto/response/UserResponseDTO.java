package com.ashutosh.backend.dto.response;

import com.ashutosh.backend.enums.UserRole;
import lombok.Builder;
import lombok.Data;

/**
 * Data Transfer Object for providing user profile information to the client.
 * This class acts as a security layer by filtering out sensitive internal data
 * such as password hashes and government identifiers, ensuring only safe,
 * display-ready information reaches the frontend.
 */
@Data
@Builder
public class UserResponseDTO {

        private Long id;
        private String firstName;
        private String lastName;
        private String email;
        private String phoneNumber;

        /**
         * The system role assigned to the user, determining their access permissions.
         */
        private UserRole role;

        /**
         * Indicates whether the user's account is active and permitted to use the system.
         */
        private Boolean isActive;
}
