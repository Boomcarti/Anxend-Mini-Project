module default {
    type Person {
        required property name -> str;
        required property age -> int16;
        required property school -> str; 
    }

    type School {
        required property name -> str;
        required property address -> str;
        required property town -> str;
    }
}
