package com.ashutosh.backend.dto.response;

import lombok.Builder;
import lombok.Data;

/**
 * Data Transfer Object sent to the client upon successful authentication.
 * It bundles the security token required for subsequent authorized requests
 * along with the user's profile details to minimize initial API round-trips.
 */
@Data
@Builder
public class LoginResponseDTO {

    /**
     * The JSON Web Token (JWT) string.
     * Acts as the bearer token that the frontend must include in the
     * Authorization header for all protected API calls.
     */
    private String token;

    /**
     * A nested object containing the authenticated user's profile information.
     * Including this in the login response allows the frontend to immediately
     * update the UI state and user context without an additional fetch.
     */
    private UserResponseDTO user;
}