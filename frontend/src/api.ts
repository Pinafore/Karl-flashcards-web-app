import axios from "axios";
import { apiUrl } from "@/env";
import { IComponents } from "./interfaces";

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    return axios.post(`${apiUrl}/api/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IComponents["User"]>(`${apiUrl}/api/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IComponents["UserUpdate"]) {
    return axios.put<IComponents["User"]>(
      `${apiUrl}/api/users/me`,
      data,
      authHeaders(token),
    );
  },
  async getUsers(token: string) {
    return axios.get<IComponents["User"][]>(`${apiUrl}/api/users/`, authHeaders(token));
  },
  async updateUser(
    token: string,
    userId: number,
    data: IComponents["SuperUserUpdate"],
  ) {
    return axios.put(`${apiUrl}/api/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IComponents["SuperUserCreate"]) {
    return axios.post(`${apiUrl}/api/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/reset-password/`, {
      new_password: password, // eslint-disable-line @typescript-eslint/camelcase
      token,
    });
  },
};
