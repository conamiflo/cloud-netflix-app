export class UserDTO {
  username: string;
  email: string;
  phone_number:number;
  name:string;
  family_name:string;
  password: string;
  constructor(username:string,name: string,email:string,password:string,phone_number:number,family_name:string ) {
    this.name = name;
    this.username=username
    this.email=email;
    this.password=password;
    this.phone_number=phone_number;
    this.family_name=family_name
  }
}
