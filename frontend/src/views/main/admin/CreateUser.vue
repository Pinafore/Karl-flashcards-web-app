<template>
  <v-container fluid>
    <validation-observer ref="observer" v-slot="{ invalid }">
      <form @submit.prevent="onSubmit" @reset.prevent="onReset">
        <v-card class="ma-3 pa-3">
          <v-card-title primary-title>
            <div class="headline primary--text">Create User</div>
          </v-card-title>
          <v-card-text>
            <template>
              <!-- username -->
              <validation-provider v-slot="{ errors }" name="Username" rules="required">
                <v-text-field
                  v-model="username"
                  label="Username"
                  :error-messages="errors[0]"
                  required
                ></v-text-field>
              </validation-provider>

              <!-- email -->
              <validation-provider
                v-slot="{ errors }"
                rules="required|email"
                name="E-mail"
              >
                <v-text-field
                  v-model="email"
                  label="E-mail"
                  type="email"
                  :error-messages="errors[0]"
                  required
                ></v-text-field>
              </validation-provider>

              <!-- is superuser -->
              <div class="subheading secondary--text text--lighten-2">
                User is superuser
                <span v-if="isSuperuser">(currently is a superuser)</span
                ><span v-else>(currently is not a superuser)</span>
              </div>
              <v-checkbox v-model="isSuperuser" label="Is Superuser"></v-checkbox>

              <!-- is active -->
              <div class="subheading secondary--text text--lighten-2">
                User is active <span v-if="isActive">(currently active)</span
                ><span v-else>(currently not active)</span>
              </div>
              <v-checkbox v-model="isActive" label="Is Active"></v-checkbox>

              <v-row align="center">
                <v-col>
                  <!-- password -->
                  <validation-provider
                    v-slot="{ errors }"
                    :debounce="100"
                    name="Password"
                    vid="password1"
                    rules="required"
                  >
                    <v-text-field
                      v-model="password1"
                      type="password"
                      label="Password"
                      :error-messages="errors"
                    ></v-text-field>
                  </validation-provider>

                  <!-- password confirmation -->
                  <validation-provider
                    v-slot="{ errors }"
                    :debounce="100"
                    name="Password confirmation"
                    vid="password2"
                    rules="required|confirmed:password1"
                  >
                    <v-text-field
                      v-model="password2"
                      type="password"
                      label="Confirm Password"
                      :error-messages="errors"
                    ></v-text-field>
                  </validation-provider>
                </v-col>
              </v-row>
            </template>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="cancel">Cancel</v-btn>
            <v-btn type="reset">Reset</v-btn>
            <v-btn type="submit" :disabled="invalid">Save</v-btn>
          </v-card-actions>
        </v-card>
      </form>
    </validation-observer>
  </v-container>
</template>

<script lang="ts">
  import { Component, Vue } from "vue-property-decorator";
  import { IComponents } from "@/interfaces";
  import { adminStore } from "@/store";
  import { required, confirmed, email } from "vee-validate/dist/rules";
  import { ValidationProvider, ValidationObserver, extend } from "vee-validate";

  // register validation rules
  extend("required", { ...required, message: "{_field_} can not be empty" });
  extend("confirmed", { ...confirmed, message: "Passwords do not match" });
  extend("email", { ...email, message: "Invalid email address" });

  @Component({
    components: {
      ValidationObserver,
      ValidationProvider,
    },
  })
  export default class CreateUser extends Vue {
    $refs!: {
      observer: InstanceType<typeof ValidationObserver>;
    };

    username = "";
    email = "";
    isActive = true;
    isSuperuser = false;
    password1 = "";
    password2 = "";

    async mounted() {
      await adminStore.getUsers();
      this.onReset();
    }

    onReset() {
      this.password1 = "";
      this.password2 = "";
      this.username = "";
      this.email = "";
      this.isActive = true;
      this.isSuperuser = false;
      this.$refs.observer.reset();
    }

    cancel() {
      this.$router.back();
    }

    async onSubmit() {
      const success = await this.$refs.observer.validate();

      if (!success) {
        return;
      }

      const updatedProfile: IComponents["SuperUserCreate"] = {
        email: this.email,
        username: this.username,
        is_active: this.isActive,
        is_superuser: this.isSuperuser,
        password: this.password1,
      };
      await adminStore.createUser(updatedProfile);
      await this.$router.push("/main/admin/users");
    }
  }
</script>
