package com.ashutosh.backend.dto.request;

import jakarta.validation.constraints.FutureOrPresent;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.time.LocalDate;

@Data
public class BookingRequestDTO {
    // The minimum a user needs to send us to reserve a car.

    // I omitted userId is INTENTIONALLY here for security.
    // It will be extracted from the secure user session/token in the Controller.

    @NotNull(message = "Vehicle ID is required")
    private Long vehicleId;

    @NotNull(message = "Start date is required")
    @FutureOrPresent(message = "Start date cannot be in the past")
    private LocalDate startDate;

    @NotNull(message = "End date is required")
    private LocalDate endDate;
}