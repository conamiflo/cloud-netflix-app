import { Routes } from '@angular/router';
import {LoginComponent} from "./features/account-managing/login/login.component";
import {RegistrationComponent} from "./features/account-managing/registration/registration.component";
import {HomePageComponent} from "./features/home/components/movies/home-page/home-page.component";

export const routes: Routes = [
  {
  path: 'login',
  component: LoginComponent
  },
  {
    path: 'registration',
    component: RegistrationComponent
  },
  {
    path: '',
    component: HomePageComponent
  },

];
