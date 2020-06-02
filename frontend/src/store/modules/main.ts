import { api } from "@/api";
import { getLocalToken, removeLocalToken, saveLocalToken } from "@/utils";
import router from "@/router";
import { AxiosError } from "axios";
import { VuexModule, Module, Mutation, Action } from "vuex-module-decorators";
import { IComponents, IAppNotification } from "@/interfaces";
import { UNAUTHORIZED } from "http-status-codes";

@Module({ name: "main" })
export default class MainModule extends VuexModule {
  token = "";
  isLoggedIn: boolean | null = null;
  logInError = false;
  signUpError = false;
  userProfile: IComponents["User"] | null = null;
  dashboardShowDrawer = true;
  notifications: IAppNotification[] = [];
  publicDecks: IComponents["Deck"][] = [];
  facts: IComponents["Fact"][] = [];

  get hasAdminAccess() {
    return (
      this.userProfile && this.userProfile.is_superuser && this.userProfile.is_active
    );
  }

  get firstNotification() {
    return this.notifications.length > 0 && this.notifications[0];
  }

  @Mutation
  setToken(payload: string) {
    this.token = payload;
  }

  @Mutation
  setLoggedIn(payload: boolean) {
    this.isLoggedIn = payload;
  }

  @Mutation
  setLogInError(payload: boolean) {
    this.logInError = payload;
  }

  @Mutation
  setSignUpError(payload: boolean) {
    this.signUpError = payload;
  }

  @Mutation
  setUserProfile(payload: IComponents["User"]) {
    this.userProfile = payload;
  }

  @Mutation
  setDashboardShowDrawer(payload: boolean) {
    this.dashboardShowDrawer = payload;
  }

  @Mutation
  addNotification(payload: IAppNotification) {
    this.notifications.push(payload);
  }

  @Mutation
  removeNotification(payload: IAppNotification) {
    this.notifications = this.notifications.filter(
      (notification) => notification !== payload,
    );
  }

  @Mutation
  setFacts(payload: IComponents["Fact"][]) {
    this.facts = payload;
  }

  @Mutation
  setPublicDecks(payload: IComponents["Deck"][]) {
    this.publicDecks = payload;
  }

  @Action
  async logIn(payload: { username: string; password: string }) {
    try {
      const response = await api.logInGetToken(payload.username, payload.password);
      const token = response.data.access_token;
      if (token) {
        saveLocalToken(token);
        this.setToken(token);
        this.setLoggedIn(true);
        this.setLogInError(false);
        await this.getUserProfile();
        await this.routeLoggedIn();
        this.addNotification({ content: "Logged in", color: "success" });
      } else {
        await this.logOut();
      }
    } catch (err) {
      this.setLogInError(true);
      await this.logOut();
    }
  }

  @Action
  async getUserProfile() {
    try {
      const response = await api.getMe(this.token);
      if (response.data) {
        this.setUserProfile(response.data);
      }
    } catch (error) {
      await this.checkApiError(error);
    }
  }

  @Action
  async updateUserProfile(payload: IComponents["UserUpdate"]) {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      this.addNotification(loadingNotification);
      const response = (
        await Promise.all([
          api.updateMe(this.token, payload),
          await new Promise((resolve, _reject) => setTimeout(() => resolve(), 500)),
        ])
      )[0];
      this.setUserProfile(response.data);
      this.removeNotification(loadingNotification);
      this.addNotification({
        content: "Profile successfully updated",
        color: "success",
      });
    } catch (error) {
      await this.checkApiError(error);
    }
  }

  @Action
  async checkLoggedIn() {
    if (!this.isLoggedIn) {
      let token = this.token;
      if (!token) {
        const localToken = getLocalToken();
        if (localToken) {
          this.setToken(localToken);
          token = localToken;
        }
      }
      if (token) {
        try {
          const response = await api.getMe(token);
          this.setLoggedIn(true);
          this.setUserProfile(response.data);
        } catch (error) {
          await this.removeLogIn();
        }
      } else {
        await this.removeLogIn();
      }
    }
  }

  @Action
  async removeLogIn() {
    removeLocalToken();
    this.setToken("");
    this.setLoggedIn(false);
  }

  @Action
  async logOut() {
    await this.removeLogIn();
    await this.routeLogOut();
  }

  @Action
  async userLogOut() {
    await this.logOut();
    this.addNotification({ content: "Logged out", color: "success" });
  }

  @Action
  async routeLogOut() {
    if (router.currentRoute.path !== "/login") {
      await router.push("/login");
    }
  }

  @Action
  async checkApiError(payload: AxiosError) {
    if (payload.response && payload.response.status === UNAUTHORIZED) {
      await this.logOut();
    }
  }

  @Action
  async routeLoggedIn() {
    if (router.currentRoute.path === "/login" || router.currentRoute.path === "/") {
      router.push("/main");
    } else if (router.currentRoute.path === "/sign-up") {
      router.push("main/add/public-decks");
    }
  }

  @Action
  async removeNotificationDelayed(payload: {
    notification: IAppNotification;
    timeout: number;
  }) {
    return new Promise((resolve, _reject) => {
      setTimeout(() => {
        this.removeNotification(payload.notification);
        resolve(true);
      }, payload.timeout);
    });
  }

  @Action
  async recoverPassword(payload: { username: string }) {
    const loadingNotification = {
      content: "Sending password recovery email",
      showProgress: true,
    };
    try {
      this.addNotification(loadingNotification);
      await Promise.all([
        api.passwordRecovery(payload.username),
        await new Promise((resolve, _reject) => setTimeout(() => resolve(), 500)),
      ]);
      this.removeNotification(loadingNotification);
      this.addNotification({
        content: "Password recovery email sent",
        color: "success",
      });
      await this.logOut();
    } catch (error) {
      this.removeNotification(loadingNotification);
      this.addNotification({ color: "error", content: "Incorrect username" });
    }
  }

  @Action
  async resetPassword(payload: { password: string; token: string }) {
    const loadingNotification = { content: "Resetting password", showProgress: true };
    try {
      this.addNotification(loadingNotification);
      await Promise.all([
        api.resetPassword(payload.password, payload.token),
        await new Promise((resolve, _reject) => setTimeout(() => resolve(), 500)),
      ]);
      this.removeNotification(loadingNotification);
      this.addNotification({
        content: "Password successfully reset",
        color: "success",
      });
      await this.logOut();
    } catch (error) {
      this.removeNotification(loadingNotification);
      this.addNotification({
        color: "error",
        content: "Error resetting password",
      });
    }
  }

  @Action
  async createUserOpen(payload: IComponents["UserCreate"]) {
    const loadingNotification = { content: "Creating account", showProgress: true };
    try {
      this.addNotification(loadingNotification);
      const response = (
        await Promise.all([
          api.createUserOpen(this.token, payload),
          await new Promise((resolve, _reject) => setTimeout(() => resolve(), 500)),
        ])
      )[0];
      this.removeNotification(loadingNotification);
      this.setSignUpError(false);
      this.addNotification({ content: "User successfully created", color: "success" });
      this.setUserProfile(response.data);
      return true;
    } catch (error) {
      this.removeNotification(loadingNotification);
      this.setSignUpError(true);
      this.addNotification({ content: "An error occurred", color: "error" });
      await this.checkApiError(error);
    }
  }

  @Action
  async createDeck(payload: IComponents["DeckCreate"]) {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      this.addNotification(loadingNotification);
      const _response = ( // eslint-disable-line
        await Promise.all([
          api.createDeck(this.token, payload),
          await new Promise((resolve, _reject) => setTimeout(() => resolve(), 500)),
        ])
      )[0];
      this.removeNotification(loadingNotification);
      this.addNotification({
        content: "Deck successfully created",
        color: "success",
      });
    } catch (error) {
      await this.checkApiError(error);
    }
  }

  @Action
  async createFact(payload: IComponents["FactCreate"]) {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      this.addNotification(loadingNotification);
      const _response = ( // eslint-disable-line
        await Promise.all([
          api.createFact(this.token, payload),
          await new Promise((resolve, _reject) => setTimeout(() => resolve(), 500)),
        ])
      )[0];
      this.removeNotification(loadingNotification);
      this.addNotification({
        content: "Fact successfully created",
        color: "success",
      });
    } catch (error) {
      await this.checkApiError(error);
    }
  }

  @Action
  async getFacts() {
    try {
      const response = await api.getFacts(this.token);
      if (response) {
        this.setFacts(response.data);
      }
    } catch (error) {
      await this.checkApiError(error);
    }
  }

  @Action
  async getPublicDecks() {
    try {
      const response = await api.getPublicDecks(this.token);
      if (response) {
        this.setPublicDecks(response.data);
      }
    } catch (error) {
      await this.checkApiError(error);
    }
  }

  @Action
  async assignDecks(payload: number[]) {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      this.addNotification(loadingNotification);
      const response = (
        await Promise.all([
          api.assignDecks(this.token, payload),
          await new Promise((resolve, _reject) => setTimeout(() => resolve(), 500)),
        ])
      )[0];
      this.setUserProfile(response.data);
      this.removeNotification(loadingNotification);
      this.addNotification({
        content: "Decks assigned",
        color: "success",
      });
    } catch (error) {
      await this.checkApiError(error);
    }
  }
}
