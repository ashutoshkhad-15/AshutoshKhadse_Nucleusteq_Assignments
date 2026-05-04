package com.ashutosh.backend.dto.request;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

/**
 * Data Transfer Object for submitting vehicle reviews and ratings.
 * Used to collect feedback from users once a rental transaction is finalized,
 * helping maintain quality standards and providing insights for other customers.
 */
@Data
public class ReviewRequestDTO {

    /**
     * The unique identifier for the completed rental transaction.
     * Links the feedback to a specific vehicle and user journey.
     */
    @NotNull(message = "Booking ID is required")
    private Long bookingId;

    /**
     * The numerical score assigned to the rental experience.
     * Enforces a standard 1-to-5 star scale for consistency in data analysis.
     */
    @NotNull(message = "Rating is required")
    @Min(value = 1, message = "Rating must be at least 1")
    @Max(value = 5, message = "Rating cannot exceed 5")
    private Integer rating;

    /**
     * Optional text-based feedback providing specific details about the experience.
     */
    private String comment;
}