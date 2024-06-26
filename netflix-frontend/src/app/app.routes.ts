import { Routes } from '@angular/router';
import {LoginComponent} from "./features/account-managing/login/login.component";
import {RegistrationComponent} from "./features/account-managing/registration/registration.component";
import {HomePageComponent} from "./features/home/components/home-page/home-page.component";
import {RoleGuard} from "./core/guards/RoleGuard";
import {MovieDetailsComponent} from "./features/home/components/movies/movie-details/movie-details.component";

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
  {
    path: 'movie',
    component: MovieDetailsComponent
  },
]
