import jax.lax
import jax.numpy as jnp
import jaxlie

import jaxsim.typing as jtp


class Quaternion:
    @staticmethod
    def to_xyzw(wxyz: jtp.Vector) -> jtp.Vector:
        """
        Convert a quaternion from WXYZ to XYZW representation.

        Args:
            wxyz (jtp.Vector): Quaternion in WXYZ representation.

        Returns:
            jtp.Vector: Quaternion in XYZW representation.
        """
        return wxyz.squeeze()[jnp.array([1, 2, 3, 0])]

    @staticmethod
    def to_wxyz(xyzw: jtp.Vector) -> jtp.Vector:
        """
        Convert a quaternion from XYZW to WXYZ representation.

        Args:
            xyzw (jtp.Vector): Quaternion in XYZW representation.

        Returns:
            jtp.Vector: Quaternion in WXYZ representation.
        """
        return xyzw.squeeze()[jnp.array([3, 0, 1, 2])]

    @staticmethod
    def to_dcm(quaternion: jtp.Vector) -> jtp.Matrix:
        """
        Convert a quaternion to a direction cosine matrix (DCM).

        Args:
            quaternion (jtp.Vector): Quaternion in XYZW representation.

        Returns:
            jtp.Matrix: Direction cosine matrix (DCM).
        """
        return jaxlie.SO3.from_quaternion_xyzw(
            xyzw=Quaternion.to_xyzw(quaternion)
        ).as_matrix()

    @staticmethod
    def from_dcm(dcm: jtp.Matrix) -> jtp.Vector:
        """
        Convert a direction cosine matrix (DCM) to a quaternion.

        Args:
            dcm (jtp.Matrix): Direction cosine matrix (DCM).

        Returns:
            jtp.Vector: Quaternion in XYZW representation.
        """
        return Quaternion.to_wxyz(
            xyzw=jaxlie.SO3.from_matrix(matrix=dcm).as_quaternion_xyzw()
        )

    @staticmethod
    def derivative(
        quaternion: jtp.Vector,
        omega: jtp.Vector,
        omega_in_body_fixed: bool = False,
        K: float = 0.1,
    ) -> jtp.Vector:
        """
        Compute the derivative of a quaternion given angular velocity.

        Args:
            quaternion (jtp.Vector): Quaternion in XYZW representation.
            omega (jtp.Vector): Angular velocity vector.
            omega_in_body_fixed (bool): Whether the angular velocity is in the body-fixed frame.
            K (float): A scaling factor.

        Returns:
            jtp.Vector: The derivative of the quaternion.
        """
        ω = omega.squeeze()
        quaternion = quaternion.squeeze()

        def Q_body(q: jtp.Vector) -> jtp.Matrix:
            qw, qx, qy, qz = q

            return jnp.array(
                [
                    [qw, -qx, -qy, -qz],
                    [qx, qw, -qz, qy],
                    [qy, qz, qw, -qx],
                    [qz, -qy, qx, qw],
                ]
            )

        def Q_inertial(q: jtp.Vector) -> jtp.Matrix:
            qw, qx, qy, qz = q

            return jnp.array(
                [
                    [qw, -qx, -qy, -qz],
                    [qx, qw, qz, -qy],
                    [qy, -qz, qw, qx],
                    [qz, qy, -qx, qw],
                ]
            )

        Q = jax.lax.cond(
            pred=omega_in_body_fixed,
            true_fun=Q_body,
            false_fun=Q_inertial,
            operand=quaternion,
        )

        norm_ω = jax.lax.cond(
            pred=ω.dot(ω) < (1e-6) ** 2,
            true_fun=lambda _: 1e-6,
            false_fun=lambda _: jnp.linalg.norm(ω),
            operand=None,
        )

        qd = 0.5 * (
            Q
            @ jnp.hstack(
                [
                    K * norm_ω * (1 - jnp.linalg.norm(quaternion)),
                    ω,
                ]
            )
        )

        return jnp.vstack(qd)

    @staticmethod
    def integration(
        quaternion: jtp.VectorLike,
        dt: jtp.FloatLike,
        omega: jtp.VectorLike,
        omega_in_body_fixed: jtp.BoolLike = False,
    ) -> jtp.Vector:
        """
        Integrate a quaternion in SO(3) given an angular velocity.

        Args:
            quaternion: The quaternion to integrate.
            dt: The time step.
            omega: The angular velocity vector.
            omega_in_body_fixed:
                Whether the angular velocity is in body-fixed representation
                as opposed to the default inertial-fixed representation.

        Returns:
            The integrated quaternion.
        """

        ω_AB = jnp.array(omega).squeeze().astype(float)
        A_Q_B = jnp.array(quaternion).squeeze().astype(float)

        # Build the initial SO(3) quaternion.
        W_Q_B_t0 = jaxlie.SO3.from_quaternion_xyzw(xyzw=Quaternion.to_xyzw(wxyz=A_Q_B))

        # Integrate the quaternion on the manifold.
        W_Q_B_tf = jax.lax.select(
            pred=omega_in_body_fixed,
            on_true=Quaternion.to_wxyz(
                xyzw=(W_Q_B_t0 @ jaxlie.SO3.exp(tangent=dt * ω_AB)).as_quaternion_xyzw()
            ),
            on_false=Quaternion.to_wxyz(
                xyzw=(jaxlie.SO3.exp(tangent=dt * ω_AB) @ W_Q_B_t0).as_quaternion_xyzw()
            ),
        )

        return W_Q_B_tf
