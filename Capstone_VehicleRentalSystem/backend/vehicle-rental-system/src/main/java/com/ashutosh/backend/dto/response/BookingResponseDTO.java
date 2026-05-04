package com.ashutosh.backend.dto.response;

import com.ashutosh.backend.enums.BookingStatus;
import com.ashutosh.backend.enums.VehicleType;
import lombok.Builder;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Data Transfer Object for sending booking details to the frontend.
 * This class provides a flattened view of the Booking entity, combining user and vehicle
 * information into a single object to simplify data binding in the UI components.
 */
@Data
@Builder
public class BookingResponseDTO {
    // Flattened object making it incredibly easy for the frontend HTML
    // to render a clean table of booking history.
    private Long   id;

    //  User snapshot
    private Long   userId;
    private String userName;   // firstName + lastName combined
    private String userEmail;

    // Vehicle snapshot
    private Long        vehicleId;
    private String      vehicleName;
    private VehicleType vehicleType;
    private String      vehicleMake;
    private String      vehicleModel;

    // Booking details
    private LocalDate     startDate;
    private LocalDate     endDate;
    private BigDecimal    totalAmount;
    private BookingStatus status;
    private LocalDateTime createdAt;
    private Boolean       isReviewed;
}