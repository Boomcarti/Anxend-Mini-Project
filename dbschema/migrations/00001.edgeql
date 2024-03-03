CREATE MIGRATION m1f2shzuese2hx7jlvy4hjrxygwyktcfwcnoeasg3luc7izbcptz5a
    ONTO initial
{
  CREATE TYPE default::Person {
      CREATE REQUIRED PROPERTY age: std::int16;
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE REQUIRED PROPERTY school: std::str;
  };
};
