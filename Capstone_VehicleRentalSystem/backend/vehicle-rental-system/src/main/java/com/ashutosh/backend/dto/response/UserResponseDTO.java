package com.ashutosh.backend.dto.response;

import com.ashutosh.backend.enums.UserRole;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class UserResponseDTO {

        // this is our security shield. Notice how I did NOT include the passwordHash
        // or the driversLicenseNumber in this response object.
        // This ensures sensitive data never accidentally leaks to the frontend's browser network tab.
        private Long id;
        private String firstName;
        private String lastName;
        private String email;
        // I included phone number and active status so the frontend profile page
        // has enough data to display the user's basic contact info.
        private String phoneNumber;
        private UserRole role;
        private Boolean isActive;
}
