package com.ashutosh.session2.component.formatter;

import org.springframework.stereotype.Component;

// We tell Spring to manage this class and specifically name it "LONG"
// so we can easily grab this exact formatter whenever someone asks for the LONG type.
@Component("LONG")
public class LongMessageFormatter implements MessageFormatter {

    // This method does the work of taking a simple string and making it look big and fancy
    @Override
    public String format(String payload) {
        // check if the message is actually there. We don't want to do all that formatting work for a blank or null string
        if (payload == null || payload.isBlank()) {
            return "[EMPTY LONG MESSAGE]";
        }
        // Here we build a nice text box using hyphen signs to wrap around our message
        return  "-".repeat(40) + "\n" +
                "LONG FORMAT MESSAGE\n"  +
                "-".repeat(40) + "\n" +
                payload                  + "\n" +
                "-".repeat(40) + "\n" +
                "[ END OF MESSAGE ]";
    }
    @Override
    public String getType() { return "LONG"; }
}
