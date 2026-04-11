package com.ashutosh.session2.component.formatter;

import org.springframework.stereotype.Component;

@Component("LONG")
public class LongMessageFormatter implements MessageFormatter {

    @Override
    public String format(String payload) {
        if (payload == null || payload.isBlank()) {
            return "[EMPTY LONG MESSAGE]";
        }
        return  "=".repeat(40) + "\n" +
                "LONG FORMAT MESSAGE\n"  +
                "=".repeat(40) + "\n" +
                payload                  + "\n" +
                "=".repeat(40) + "\n" +
                "[ END OF MESSAGE ]";
    }
    @Override
    public String getType() { return "LONG"; }
}
