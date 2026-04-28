package com.ashutosh.backend.security;

import com.ashutosh.backend.entity.AppUser;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.security.Key;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

/**
 * Handles the generation, parsing, and cryptographic validation of JSON Web Tokens (JWT).
 * Acts as the primary utility for securing stateless authentication sessions by managing
 * token lifecycles and payload data.
 */
@Service
public class JwtService {

    @Value("${jwt.secret}")
    private String secretKey;

    @Value("${jwt.expiration}")
    private long jwtExpiration;

    /**
     * Constructs a secure JSON Web Token for an authenticated user.
     * Embeds necessary authorization claims, specifically the user's system role,
     * to facilitate client-side routing and backend authorization checks. Signs the
     * payload cryptographically using the configured secret key.
     *
     * @param user The authenticated user entity requiring a session token.
     * @return A signed and serialized JWT string.
     */
    public String generateToken(AppUser user) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("role", user.getRole().name());

        return Jwts.builder()
                .setClaims(claims)
                .setSubject(user.getEmail())
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + jwtExpiration))
                .signWith(getSignInKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    /**
     * Retrieves the subject identifier (email address) embedded within the provided token.
     *
     * @param token The JSON Web Token string.
     * @return The extracted user email.
     */
    public String extractEmail(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    /**
     * Evaluates the authenticity and lifecycle of a token.
     * Verifies that the extracted email matches the provided user identity and confirms
     * the token has not expired. Safely catches cryptographic parsing exceptions to
     * deny access gracefully without causing system-wide failures.
     *
     * @param token The JSON Web Token presented by the client.
     * @param userEmail The expected email address of the authenticated user.
     * @return True if the token is valid, unaltered, and unexpired; false otherwise.
     */
    public boolean isTokenValid(String token, String userEmail) {
        try {
            final String extractedEmail = extractEmail(token);
            return extractedEmail.equals(userEmail) && !isTokenExpired(token);
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * Determines if the token's expiration timestamp precedes the current system time.
     *
     * @param token The JSON Web Token to evaluate.
     * @return True if the token has expired; false otherwise.
     */
    private boolean isTokenExpired(String token) {
        return extractClaim(token, Claims::getExpiration).before(new Date());
    }

    /**
     * Parses the token payload to resolve specific cryptographic claims.
     * Applies the provided functional resolver to extract the desired data point
     * from the token's body.
     *
     * @param token The JSON Web Token string.
     * @param resolver The functional interface defining which claim to extract.
     * @param <T> The expected return type of the requested claim.
     * @return The extracted claim value.
     */
    private <T> T extractClaim(String token, Function<Claims, T> resolver) {
        Claims claims = Jwts.parserBuilder()
                .setSigningKey(getSignInKey())
                .build()
                .parseClaimsJws(token)
                .getBody();
        return resolver.apply(claims);
    }

    /**
     * Converts the Base64-encoded secret property into a cryptographic signing key.
     *
     * @return A secure HMAC-SHA key used for token signature generation and verification.
     */
    private Key getSignInKey() {
        byte[] keyBytes = Decoders.BASE64.decode(secretKey);
        return Keys.hmacShaKeyFor(keyBytes);
    }
}