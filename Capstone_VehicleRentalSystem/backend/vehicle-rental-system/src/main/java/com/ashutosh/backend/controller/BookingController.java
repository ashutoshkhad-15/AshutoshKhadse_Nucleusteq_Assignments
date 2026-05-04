package com.ashutosh.backend.controller;

import com.ashutosh.backend.dto.request.BookingRequestDTO;
import com.ashutosh.backend.dto.response.BookingResponseDTO;
import com.ashutosh.backend.service.BookingService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST controller responsible for handling vehicle rental operations.
 * Exposes endpoints for users to create and manage their bookings,
 * and for administrators to oversee platform activity.
 */
@RestController
@RequestMapping("/api/bookings")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
@Slf4j
public class BookingController {

    private final BookingService bookingService;

    /**
     * Processes a request to create a new vehicle rental booking.
     * Extracts the user's identity from the active security context to associate the booking securely.
     *
     * @param request The booking details provided by the frontend.
     * @param authentication The current Spring Security context.
     * @return ResponseEntity containing the finalized booking details and a 201 Created status.
     */
    @PostMapping
    public ResponseEntity<BookingResponseDTO> createBooking(@Valid @RequestBody BookingRequestDTO request, Authentication authentication) {
        String userEmail = extractEmail(authentication);
        log.info("REST request received: Create booking for vehicle ID: {} by user: {}", request.getVehicleId(), userEmail);

        BookingResponseDTO response = bookingService.createBooking(request, userEmail);

        log.info("Successfully processed booking request. Returned booking ID: {}", response.getId());
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    /**
     * Retrieves the complete booking history for the currently authenticated user.
     *
     * @param authentication The current Spring Security context.
     * @return ResponseEntity containing a list of the user's bookings.
     */
    @GetMapping("/my-bookings")
    public ResponseEntity<List<BookingResponseDTO>> getMyBookings(Authentication authentication) {
        String userEmail = extractEmail(authentication);
        log.info("REST request received: Fetch booking history for user: {}", userEmail);

        List<BookingResponseDTO> response = bookingService.getUserBookings(userEmail);
        return ResponseEntity.ok(response);
    }

    /**
     * Processes a user's request to cancel an existing booking.
     *
     * @param id The unique identifier of the booking to cancel.
     * @param authentication The current Spring Security context.
     * @return ResponseEntity containing the updated booking status.
     */
    @PutMapping("/{id}/cancel")
    public ResponseEntity<BookingResponseDTO> cancelBooking(@PathVariable Long id, Authentication authentication) {
        String userEmail = extractEmail(authentication);
        log.info("REST request received: Cancel booking ID: {} requested by user: {}", id, userEmail);

        BookingResponseDTO response = bookingService.cancelBooking(id, userEmail);
        return ResponseEntity.ok(response);
    }

    /**
     * Retrieves all bookings across the platform for administrative oversight.
     *
     * @return ResponseEntity containing the complete list of system bookings.
     */
    @GetMapping("/admin/all")
    public ResponseEntity<List<BookingResponseDTO>> getAllBookingsAdmin() {
        log.info("REST request received: Fetch all system bookings (Admin Access).");

        List<BookingResponseDTO> response = bookingService.getAllBookingsForAdmin();
        return ResponseEntity.ok(response);
    }

    /**
     * Processes an administrative request to manually mark a booking as completed
     * upon the successful return of a vehicle.
     *
     * @param id The unique identifier of the booking to finalize.
     * @return ResponseEntity containing the updated booking details.
     */
    @PutMapping("/admin/{id}/complete")
    public ResponseEntity<BookingResponseDTO> completeBooking(@PathVariable Long id) {
        log.info("REST request received: Mark booking ID: {} as COMPLETED (Admin Access).", id);

        BookingResponseDTO response = bookingService.completeBooking(id);
        return ResponseEntity.ok(response);
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