import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Box,
  Button,
  TextField,
  InputAdornment,
  IconButton,
  Alert,
  CircularProgress,
} from "@mui/material";
import PersonOutlineIcon from "@mui/icons-material/PersonOutline";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import { useState } from "react";
import { loginSchema, type LoginFormValues } from "../schemas/auth.schema";
import { useLoginMutation } from "../mutations/use-login-mutation";

export function LoginForm() {
  const [showPassword, setShowPassword] = useState(false);
  const { mutate, isPending, error } = useLoginMutation();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = (values: LoginFormValues) => {
    mutate({ username: values.username, password: values.password });
  };

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error.message}
        </Alert>
      )}

      <TextField
        {...register("username")}
        label="Username"
        fullWidth
        autoFocus
        autoComplete="username"
        margin="normal"
        error={Boolean(errors.username)}
        helperText={errors.username?.message}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <PersonOutlineIcon color="action" />
            </InputAdornment>
          ),
        }}
      />

      <TextField
        {...register("password")}
        label="Password"
        type={showPassword ? "text" : "password"}
        fullWidth
        autoComplete="current-password"
        margin="normal"
        error={Boolean(errors.password)}
        helperText={errors.password?.message}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <LockOutlinedIcon color="action" />
            </InputAdornment>
          ),
          endAdornment: (
            <InputAdornment position="end">
              <IconButton
                onClick={() => setShowPassword((v) => !v)}
                edge="end"
                aria-label="toggle password visibility"
              >
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          ),
        }}
      />

      <Button
        type="submit"
        fullWidth
        variant="contained"
        size="large"
        disabled={isPending}
        sx={{ mt: 2, py: 1.5, fontWeight: 700 }}
      >
        {isPending ? <CircularProgress size={22} color="inherit" /> : "Sign In"}
      </Button>
    </Box>
  );
}
