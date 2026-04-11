package com.ashutosh.session2.component.formatter;

public interface MessageFormatter {

    // This method will take the raw message text and change how it looks based on the specific formatter we use
    String format(String payload);
    // This method tells us what kind of formatter we are dealing with (like "SHORT" or "LONG").
    String getType();
}
