package com.ashutosh.backend.dto.response;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class LoginResponseDTO {

    // I am including the auth token here so the frontend has the "ticket"
    // it needs to securely make future API requests.
    private String token;

    // instead of forcing the UI to make a second API call to fetch the profile,
    // I am nesting the UserResponseDTO right here. This drastically simplifies my frontend state management
    private UserResponseDTO user;
}
