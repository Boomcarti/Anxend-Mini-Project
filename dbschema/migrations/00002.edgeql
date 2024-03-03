CREATE MIGRATION m1aykrhpkwotvqlmuewt2njkrkvn4munwjolr7gsiyvrwupfsgr2rq
    ONTO m1f2shzuese2hx7jlvy4hjrxygwyktcfwcnoeasg3luc7izbcptz5a
{
  CREATE TYPE default::School {
      CREATE REQUIRED PROPERTY address: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE REQUIRED PROPERTY town: std::str;
  };
};
