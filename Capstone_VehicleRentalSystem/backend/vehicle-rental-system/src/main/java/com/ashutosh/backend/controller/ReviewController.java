package com.ashutosh.backend.controller;

import com.ashutosh.backend.dto.request.ReviewRequestDTO;
import com.ashutosh.backend.dto.response.ReviewResponseDTO;
import com.ashutosh.backend.service.ReviewService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST controller responsible for handling the customer review system.
 * Manages incoming HTTP requests to post new reviews, fetch public reviews for vehicles,
 * and process review deletions.
 */
@RestController
@RequestMapping("/api/reviews")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
@Slf4j
public class ReviewController {

    private final ReviewService reviewService;

    /**
     * Processes a request to submit a new review for a completed vehicle rental.
     * Extracts the user's email from the security context to associate the review with the correct account.
     *
     * @param request The review details (rating, comment) provided by the frontend.
     * @param authentication The current Spring Security context.
     * @return ResponseEntity containing the finalized review details and a 201 Created status.
     */
    @PostMapping
    public ResponseEntity<ReviewResponseDTO> addReview(
            @Valid @RequestBody ReviewRequestDTO request,
            Authentication authentication) {

        String userEmail = extractEmail(authentication);
        log.info("REST request received: Add review for booking ID: {} by user: {}", request.getBookingId(), userEmail);

        ReviewResponseDTO response = reviewService.addReview(request, userEmail);

        log.info("Successfully processed review submission. Returned review ID: {}", response.getId());
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    /**
     * Retrieves all public reviews associated with a specific vehicle.
     * Intended for display on the vehicle details page in the user interface.
     *
     * @param vehicleId The unique identifier of the vehicle being queried.
     * @return ResponseEntity containing a list of the vehicle's reviews.
     */
    @GetMapping("/vehicle/{vehicleId}")
    public ResponseEntity<List<ReviewResponseDTO>> getVehicleReviews(@PathVariable Long vehicleId) {
        log.info("REST request received: Fetch all reviews for vehicle ID: {}", vehicleId);

        return ResponseEntity.ok(reviewService.getVehicleReviews(vehicleId));
    }

    /**
     * Processes a request to delete an existing review.
     * Relies on the service layer to enforce authorization rules (user ownership or admin rights).
     *
     * @param id The unique identifier of the review to delete.
     * @param authentication The current Spring Security context.
     * @return ResponseEntity with a 204 No Content status upon successful deletion.
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReview(@PathVariable Long id, Authentication authentication) {
        String userEmail = extractEmail(authentication);
        log.info("REST request received: Delete review ID: {} requested by user: {}", id, userEmail);

        reviewService.deleteReview(id, userEmail);

        log.info("Successfully processed deletion for review ID: {}", id);
        return ResponseEntity.noContent().build(); // Returns a clean 204 No Content status
    }

    /**
     * Helper method to safely extract the user's email address from the security context,
     * regardless of how the principal was instantiated by Spring Security.
     *
     * @param authentication The current Spring Security context.
     * @return The extracted email address as a String.
     */
    private String extractEmail(Authentication authentication) {
        Object principal = authentication.getPrincipal();
        if (principal instanceof com.ashutosh.backend.entity.AppUser) {
            return ((com.ashutosh.backend.entity.AppUser) principal).getEmail();
        } else if (principal instanceof org.springframework.security.core.userdetails.UserDetails) {
            return ((org.springframework.security.core.userdetails.UserDetails) principal).getUsername();
        } else {
            return principal.toString();
        }
    }
}