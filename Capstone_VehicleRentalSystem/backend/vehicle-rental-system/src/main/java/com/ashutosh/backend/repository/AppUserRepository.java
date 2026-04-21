package com.ashutosh.backend.repository;

import com.ashutosh.backend.entity.AppUser;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface AppUserRepository extends JpaRepository<AppUser, Long> {
    // I added this method so we can look up a user by their email during the login process.
    // Using Optional prevents NullPointerExceptions if the user types the wrong email.
    Optional<AppUser> findByEmail(String email);

    //this is to check if a phone number or license is already registered before creating a new account.
    boolean existsByEmail(String email);
    boolean existsByDriversLicenseNumber(String driversLicenseNumber);
}