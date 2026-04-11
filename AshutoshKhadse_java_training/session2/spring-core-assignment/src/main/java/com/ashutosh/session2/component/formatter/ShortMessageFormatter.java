package com.ashutosh.session2.component.formatter;

import org.springframework.stereotype.Component;

@Component("SHORT")
public class ShortMessageFormatter implements MessageFormatter {

    @Override
    public String format(String payload) {
        if (payload == null || payload.isBlank()) {
            return "[EMPTY SHORT MESSAGE]";
        }
        String trimmed = payload.length() > 20
                ? payload.substring(0, 20) + "..."
                : payload;
        return "SHORT >> " + trimmed;
    }
    @Override
    public String getType() { return "SHORT"; }
}

