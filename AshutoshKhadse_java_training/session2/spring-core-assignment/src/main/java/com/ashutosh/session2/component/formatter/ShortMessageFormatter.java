package com.ashutosh.session2.component.formatter;

import org.springframework.stereotype.Component;

// Telling Spring to create an object for this class and giving it the specific name "SHORT"
@Component("SHORT")
public class ShortMessageFormatter implements MessageFormatter {

    @Override
    public String format(String payload) {
        // check if the string is empty or null
        if (payload == null || payload.isBlank()) {
            return "[EMPTY SHORT MESSAGE]";
        }
        // If the message is more than 20 characters, we chop off the extra part
        // and add "..." at the end so it fits nicely. 
        String trimmed = payload.length() > 20
                ? payload.substring(0, 20) + "..."
                : payload;
        return "SHORT >> " + trimmed;
    }
    @Override
    public String getType() { return "SHORT"; }
}

