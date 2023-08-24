import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CartComponent } from './pages/welcome/container/cart/cart.component';
import { HeaderComponent } from './pages/welcome/scene/header/header.component';
import { OrderviewComponent } from './pages/welcome/orderitem/orderview/orderview.component';
import { LoginpageComponent } from './pages/welcome/logincheck/loginpage/loginpage.component';
const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: '/welcome' },
  { path: 'welcome', loadChildren: () => import('./pages/welcome/welcome.module').then(m => m.WelcomeModule) },
  {path:'cart',component:CartComponent},
  {path:'header',component:HeaderComponent},
  {path:'orderitemview',component:OrderviewComponent},
  {path:'login',component:LoginpageComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
